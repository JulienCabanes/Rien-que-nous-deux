#!/usr/bin/env python3
"""Build the site from the story sources.

    python3 tools/build.py            # writes index.html (and en/index.html…)
    python3 tools/build.py --out DIR

Every story/<lang>/book.json is one edition of the story; its chapters are
the story/<lang>/*.txt files, read in file name order. The cast
(story/cast.json) and the avatars (assets/avatars/<id>.svg|png) are shared by
all editions. The format of the chapter files is described in README.md.
"""
import base64
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StoryError(Exception):
    pass


def load_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        raise StoryError('%s: %s' % (os.path.relpath(path, ROOT), e))


def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- inline text

BOLD = re.compile(r'(?<!\*)\*\*(?!\*)(\S(?:.*?\S)?)(?<!\*)\*\*(?!\*)')
ITALIC = re.compile(r'(?<![\w_])_(?!_)(\S(?:.*?\S)?)_(?![\w_])')


NBSP, NNBSP = '\u00a0', '\u202f'
TYPOGRAPHY = None  # set per edition from book.json "typography"


def typo(text):
    """French typography: non-breaking spaces where a line must not break."""
    if TYPOGRAPHY != 'fr':
        return text
    s = re.sub(r' ([?!;»])', NNBSP + r'\1', text)          # espace fine insécable
    s = s.replace('« ', '«' + NNBSP)
    s = re.sub(r' :(?=\s|$|\*)', NBSP + ':', s)             # espace insécable
    s = re.sub(r'(\d) h (?=\d)', r'\1' + NBSP + 'h' + NBSP, s)  # 17 h 12
    s = re.sub(r'(\d) (?=(h|min|s|%|€)\b|%|€)', r'\1' + NBSP, s)  # 17 h, 43 min, 71 %, 90 €
    s = re.sub(r'(?<=\d) (?=\d{3}\b)', NBSP, s)               # 11 000
    return s


def inline(text, mention_re=None):
    """Escape text, then apply **bold** and @mentions."""
    text = typo(text)
    s = BOLD.sub(r'<strong>\1</strong>', esc(text))
    if mention_re:
        s = mention_re.sub(r'<span class="mention">\1</span>', s)
    return s


def prose(text):
    """Book-level text (intro, disclaimer): **bold** and _italic_."""
    return ITALIC.sub(r'<em>\1</em>', inline(text))


# ---------------------------------------------------------------- avatars

PALETTE = ['#5B6C8F', '#7A5C61', '#4F7A6B', '#8A6D3B', '#6B5B95', '#3E7C8C',
           '#8C5A45', '#5E7D4F', '#76507A', '#4D6A86', '#8A4F5E', '#5C6B73']


def palette(cid):
    return PALETTE[sum(map(ord, cid)) % len(PALETTE)]


def letter_avatar(name, color):
    """Initial on a colored square, for characters without an image."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 144 144">'
            '<rect width="144" height="144" fill="%s"/>'
            '<text x="72" y="72" dy=".35em" text-anchor="middle" fill="#fff" font-size="84" font-weight="700" '
            'font-family="Lato, Helvetica, Arial, sans-serif">%s</text></svg>') % (attr(color), esc(name[:1].upper()))


# ---------------------------------------------------------------- the edition

class Edition:
    def __init__(self, book_path, cast):
        self.dir = os.path.dirname(book_path)
        self.book = load_json(book_path)
        self.ui = self.book['ui']
        global TYPOGRAPHY
        TYPOGRAPHY = self.book.get('typography')
        self.cast = {k: dict(v) for k, v in cast.items()}
        self.channels = self.book['channels']
        for cid, ch in self.channels.items():
            if ch.get('workspace') not in self.book['workspaces']:
                raise StoryError('book.json: channel %s has an unknown workspace' % cid)
            for m in ch.get('members', []):
                self.need_cast(m, 'book.json: channel %s' % cid)
        names = sorted((c['name'] for c in self.cast.values()), key=len, reverse=True)
        self.mention_re = re.compile(r'(?<![\w.])(@(?:%s))(?![\w-])' % '|'.join(map(re.escape, names)))

        self.scenes = []            # [{channel, topic, count}]
        self.channel = None         # current channel id
        self.state = {}             # channel id -> {topic, count}
        self.marked = None          # last scene given a marker
        self.chapter_ids = set()
        self.out = []
        self.stats = dict(messages=0, chapters=0)

    # -- helpers

    def need_cast(self, cid, where):
        if cid not in self.cast:
            raise StoryError('%s: unknown character "%s" (known: %s)'
                             % (where, cid, ', '.join(sorted(self.cast))))
        return self.cast[cid]

    def title_html(self, cid, banner=False):
        ch = self.channels[cid]
        name = esc(ch.get('name', cid))
        kind = ch['kind']
        if kind == 'public':
            return '#' + name
        icon = {'private': '🔒', 'shared': '🤝'}[kind]
        if banner or kind == 'shared':
            return icon + ' ' + name
        return '<span class="lock">%s</span>%s' % (icon, name)

    def fill(self, template, cid):
        ch = self.channels[cid]
        ws = self.book['workspaces'][ch['workspace']]['name']
        return template.format(count=self.state[cid]['count'], workspace=ws)

    def channel_state(self, cid):
        if cid not in self.state:
            ch = self.channels[cid]
            self.state[cid] = dict(topic=ch.get('topic'), count=ch['count'],
                                   present=list(self.initially[cid]))
        return self.state[cid]

    def move(self, cid, ids, joining, where):
        """People join or leave a channel: member count and header avatars follow."""
        st = self.channel_state(cid)
        for i in ids:
            self.need_cast(i, where)
            st['count'] += 1 if joining else -1
            if joining and i not in st['present']:
                st['present'].append(i)
            if not joining and i in st['present']:
                st['present'].remove(i)

    def scene(self):
        s = self.state[self.channel]
        shown = [m for m in self.shown[self.channel] if m in s['present']]
        default = self.ui.get('topic_one', self.ui['topic']) if s['count'] == 1 else self.ui['topic']
        return dict(channel=self.channel, topic=s['topic'] or self.fill(default, self.channel),
                    count=s['count'], avatars=shown, many=self.crowded[self.channel])

    def emit(self, block):
        """Append a block; tag it if the scene changed since the last tag."""
        cur = self.scene()
        if cur != self.marked:
            self.scenes.append(cur)
            self.marked = cur
            if len(self.scenes) > 1:
                block = block.replace('>', ' data-scene="%d">' % (len(self.scenes) - 1), 1)
        self.out.append(block)

    # -- parsing

    def prescan(self, texts):
        """Who speaks in each channel, and who arrives there later.

        The header shows everyone who ever speaks in a channel (Slackbot aside);
        someone whose first move in a channel is a join is absent until then.
        """
        order, speaks, first_move = {}, {}, {}
        channel = None
        for text in texts:
            for block in re.split(r'\n\s*\n', text):
                lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
                if not lines:
                    continue
                if re.match(r'#\s|---|\[', lines[0]):
                    for l in lines:
                        m = re.match(r'\[channel (\S+)\]', l)
                        if m:
                            channel = m.group(1)
                        m = re.match(r'\[members (\S+) (.*)\]', l)
                        if m:
                            for p in m.group(2).split():
                                first_move.setdefault((m.group(1), p[1:]), p[0] == '+')
                    continue
                head = lines[0].split()
                if len(head) < 2 or channel is None:
                    continue
                who, opts = head[0], head[2:]
                moving = 'join' in opts or 'leave' in opts
                for i in [who] + [o[1:] for o in opts if o.startswith('+')]:
                    order.setdefault(channel, [])
                    if i not in order[channel]:
                        order[channel].append(i)
                    if moving:
                        first_move.setdefault((channel, i), 'join' in opts)
                if not moving and self.cast.get(who, {}).get('header', True):
                    speaks.setdefault(channel, set()).add(who)
        self.shown, self.initially = {}, {}
        # a channel that ever shows more than 7 avatars overlaps them from the start
        self.crowded = {cid: False for cid in self.channels}
        for cid, ch in self.channels.items():
            listed = list(ch.get('members', []))
            extra = [i for i in order.get(cid, []) if i in speaks.get(cid, ()) and i not in listed]
            # people first (order of appearance), then the bots, the two agents last
            self.shown[cid] = sorted(listed + extra, key=lambda i: self.cast.get(i, {}).get('header_rank', 0))
            self.initially[cid] = ch['present'] if 'present' in ch else [
                i for i in self.shown[cid] if first_move.get((cid, i)) is not True]

    def build(self):
        files = sorted(glob.glob(os.path.join(self.dir, '*.txt')))
        if not files:
            raise StoryError('%s: no chapter files' % os.path.relpath(self.dir, ROOT))
        texts = []
        for path in files:
            with open(path, encoding='utf-8') as f:
                texts.append(f.read())
        self.prescan(texts)
        for path in files:
            with open(path, encoding='utf-8') as f:
                self.parse(os.path.relpath(path, ROOT), f.read())
        for sc in self.scenes:
            if len(sc['avatars']) > 7:
                self.crowded[sc['channel']] = True
        for sc in self.scenes:
            sc['many'] = self.crowded[sc['channel']]
        return self.page()

    def parse(self, fname, text):
        lines = text.split('\n')
        i = 0
        while i < len(lines):
            if not lines[i].strip():
                i += 1
                continue
            start = i
            while i < len(lines) and lines[i].strip():
                i += 1
            block = [l.rstrip() for l in lines[start:i]]
            where = '%s:%d' % (fname, start + 1)
            try:
                if re.match(r'#\s|---|\[', block[0]):
                    for n, line in enumerate(block):
                        self.directive(line, '%s:%d' % (fname, start + 1 + n), fname)
                else:
                    self.message(block, where)
            except StoryError:
                raise
            except (KeyError, ValueError) as e:
                raise StoryError('%s: %s' % (where, e))

    def directive(self, line, where, fname):
        if line.startswith('# '):
            m = re.fullmatch(r'# (.+?) \| (.+?)(?: \{#([\w-]+)\})?', line)
            if not m:
                raise StoryError('%s: chapter heading must read "# Title | Subtitle {#id}"' % where)
            d1, d2, cid = m.groups()
            d1, d2 = typo(d1), typo(d2)
            cid = cid or re.sub(r'^\d+-', '', os.path.splitext(os.path.basename(fname))[0])
            if cid in self.chapter_ids:
                raise StoryError('%s: chapter id "%s" is already used' % (where, cid))
            self.chapter_ids.add(cid)
            self.stats['chapters'] += 1
            if self.stats['chapters'] == 1:
                self.first_chapter = '%s · %s' % (d1, d2)
            self.need_channel(where)
            self.emit('<div class="daymark" id="%s" data-d1="%s" data-d2="%s"><span class="d1">%s</span><span class="d2">%s</span></div>'
                      % (cid, attr(d1), attr(d2), esc(d1), esc(d2)))
            return
        if line.startswith('---'):
            label = line[3:].strip()
            if not label:
                raise StoryError('%s: a divider needs a label: "--- Le lendemain"' % where)
            self.need_channel(where)
            self.emit('<div class="divider"><span>%s</span></div>' % esc(typo(label)))
            return
        m = re.fullmatch(r'\[(\w+)\]\s*(.*)|\[(\w+) ([^\]]*)\]', line)
        if not m:
            raise StoryError('%s: not a directive: %s' % (where, line))
        kw = m.group(1) or m.group(3)
        arg = (m.group(2) if m.group(1) else m.group(4)).strip()
        if kw == 'channel':
            if arg not in self.channels:
                raise StoryError('%s: unknown channel "%s" (known: %s)' % (where, arg, ', '.join(self.channels)))
            self.channel = arg
            self.channel_state(arg)
        elif kw == 'banner':
            self.need_channel(where)
            sub = self.fill(self.channels[self.channel].get('banner', self.ui['banner']), self.channel)
            self.emit('<div class="chanbanner"><div class="cb1">%s</div><div class="cb2">%s</div></div>'
                      % (self.title_html(self.channel, banner=True), esc(typo(sub))))
        elif kw == 'topic':
            self.need_channel(where)
            self.state[self.channel]['topic'] = typo(arg)
        elif kw == 'cast':
            parts = arg.split()
            c = self.need_cast(parts[0] if parts else '', where)
            for kv in parts[1:]:
                k, _, v = kv.partition('=')
                if k not in ('name', 'badge', 'status', 'emoji', 'color') or not v:
                    raise StoryError('%s: expected key=value with key among name, badge, status, emoji, color' % where)
                if v == 'none':
                    c.pop(k, None)
                else:
                    c[k] = v
        elif kw == 'members':
            parts = arg.split()
            if not parts or parts[0] not in self.channels or not all(re.fullmatch(r'[+-]\w+', p) for p in parts[1:]):
                raise StoryError('%s: expected [members <channel> +id -id …]' % where)
            for p in parts[1:]:
                self.move(parts[0], [p[1:]], p[0] == '+', where)
        elif kw == 'spacer':
            self.emit('<div class="whitespace" aria-hidden="true"></div>')
        elif kw == 'interlude':
            self.need_channel(where)
            self.emit('<div class="interlude"><span>%s</span></div>' % esc(typo(arg)))
        else:
            raise StoryError('%s: unknown directive [%s]' % (where, kw))

    def need_channel(self, where):
        if not self.channel:
            raise StoryError('%s: the story must start with [channel ...]' % where)

    def message(self, block, where):
        self.need_channel(where)
        head = block[0].split()
        if len(head) < 2 or not re.fullmatch(r'\d{1,2}:\d{2}', head[1]):
            raise StoryError('%s: a message starts with "<character> <HH:MM>", got: %s' % (where, block[0]))
        c = self.need_cast(head[0], where)
        opts = [o for o in head[2:] if not o.startswith('+')]
        others = [o[1:] for o in head[2:] if o.startswith('+')]
        for o in opts:
            if o not in ('big', 'event', 'join', 'leave'):
                raise StoryError('%s: unknown message option "%s" (big, event, join, leave, +id)' % (where, o))
        if 'join' in opts or 'leave' in opts:
            # the author, plus anyone joining or leaving with them: "claude 11:07 join +chatgpt"
            self.move(self.channel, [head[0]] + others, 'join' in opts, where)
        elif others:
            raise StoryError('%s: +%s only makes sense with join or leave' % (where, others[0]))
        hh, mm = head[1].split(':')

        if 'emoji' in c:
            bg = ' style="background:%s"' % attr(c['color']) if 'color' in c else ''
            avatar = '<div class="avatar emoji"%s>%s</div>' % (bg, esc(c['emoji']))
        else:
            avatar = '<div class="avatar av-%s"></div>' % head[0]
        top = '<span class="name">%s</span>' % esc(c['name'])
        if 'status' in c:
            top += '<span class="status">%s</span>' % esc(c['status'])
        if 'badge' in c:
            top += '<span class="app">%s</span>' % esc(self.ui['badges'][c['badge']])
        h = int(hh)
        clock = self.ui['time'].format(h=hh, m=mm, h12=h % 12 or 12, ampm='AM' if h < 12 else 'PM')
        top += '<span class="time">%s</span>' % esc(typo(clock))

        cls = 'text' + (' big' if 'big' in opts else '') + (' event' if 'event' in opts else '')
        body, para, reacts = [], [], ''

        def flush():
            if para:
                body.append('<div class="%s">%s</div>' % (cls, '<br>'.join(inline(p, self.mention_re) for p in para)))
                del para[:]

        for line in block[1:]:
            if line.startswith('[thinking]'):
                label, _, meta = line[10:].partition('|')
                body.append('<div class="thinking"><span class="dots">%s</span><span class="meta">%s</span></div>'
                            % (esc(typo(label.strip())), esc(typo(meta.strip()))))
            elif line == '[next]':
                flush()
            elif line.startswith('[reactions]'):
                reacts = '<div class="reacts">%s</div>' % ''.join(
                    '<span class="react">%s</span>' % esc(r.strip()) for r in line[11:].split(',') if r.strip())
            else:
                if reacts:
                    raise StoryError('%s: [reactions] must be the last line of the message' % where)
                para.append(line)
        flush()
        if not body:
            raise StoryError('%s: empty message' % where)
        self.stats['messages'] += 1
        self.emit('<div class="msg">%s<div class="body"><div class="head">%s</div>%s%s</div></div>'
                  % (avatar, top, ''.join(body), reacts))

    # -- page

    def sidebar(self, wid, ws):
        out = ['<div data-ws="%s">' % wid]
        out.append('  <div class="section">%s</div>' % esc(self.ui['channels']))
        for item in ws.get('channels', []):
            item = item if isinstance(item, dict) else {'channel': item}
            cid = item['channel']
            if cid in self.channels:
                ch = self.channels[cid]
                icon = {'public': '#', 'private': '🔒', 'shared': '🤝'}[ch['kind']]
                extra = ' data-channel="%s"' % cid + (' data-only-active' if item.get('only_active') else '')
                if item.get('from_creation'):
                    # listed from the first scene set in the channel onwards
                    first = next((n for n, sc in enumerate(self.scenes) if sc['channel'] == cid), len(self.scenes))
                    extra += ' data-from="%d"' % first + (' style="display:none"' if first > 0 else '')
                label = ch.get('name', cid)
            else:
                icon, extra, label = '#', '', cid
            out.append('  <div class="chan"%s><span class="h">%s</span>%s</div>' % (extra, icon, esc(label)))
        if ws.get('direct_messages'):
            out.append('  <div class="section">%s</div>' % esc(self.ui['direct_messages']))
            for item in ws['direct_messages']:
                item = item if isinstance(item, dict) else {'cast': item}
                c = self.need_cast(item['cast'], 'book.json: workspace %s' % wid)
                pres = 'pres gone' if item.get('away') else 'pres'
                out.append('  <div class="chan"><span class="%s"></span>%s</div>' % (pres, esc(c['name'])))
        if ws.get('apps'):
            out.append('  <div class="section">%s</div>' % esc(self.ui['apps']))
            for cid in ws['apps']:
                c = self.need_cast(cid, 'book.json: workspace %s' % wid)
                out.append('  <div class="chan"><span class="ic" style="background:%s"></span>%s</div>'
                           % (attr(c.get('color', '#FFFFFF')), esc(c['name'])))
        out.append('</div>')
        return '\n'.join(out)

    def avatars_css(self):
        rules = []
        for cid in sorted(self.cast):
            for ext, mime in (('svg', 'image/svg+xml'), ('png', 'image/png')):
                p = os.path.join(ROOT, 'assets', 'avatars', '%s.%s' % (cid, ext))
                if os.path.exists(p):
                    with open(p, 'rb') as f:
                        b64 = base64.b64encode(f.read()).decode()
                    rules.append('.av-%s{background-image:url(data:%s;base64,%s)}' % (cid, mime, b64))
                    break
            else:
                c = self.cast[cid]
                if 'emoji' in c:
                    # message avatars show the emoji as text; the header needs an image
                    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 144 144">'
                           '<rect width="144" height="144" fill="%s"/>'
                           '<text x="72" y="72" dy=".35em" text-anchor="middle" font-size="96">%s</text></svg>'
                           % (attr(c.get('color', '#FFFFFF')), esc(c['emoji'])))
                    rules.append('.av-%s{background-image:url(data:image/svg+xml;base64,%s)}'
                                 % (cid, base64.b64encode(svg.encode()).decode()))
                else:
                    svg = letter_avatar(self.cast[cid]['name'], self.cast[cid].get('color') or palette(cid))
                    rules.append('.av-%s{background-image:url(data:image/svg+xml;base64,%s)}'
                                 % (cid, base64.b64encode(svg.encode()).decode()))
        return '\n'.join(rules)

    def page(self):
        def tpl(name):
            with open(os.path.join(ROOT, 'templates', name), encoding='utf-8') as f:
                return f.read()

        channels = {}
        for cid, ch in self.channels.items():
            channels[cid] = dict(workspace=ch['workspace'], title=self.title_html(cid))
        data = dict(scenes=self.scenes, channels=channels,
                    workspaces={k: v['name'] for k, v in self.book['workspaces'].items()})
        first = self.scenes[0]
        first_ch = channels[first['channel']]
        sidebars = []
        for wid, ws in self.book['workspaces'].items():
            sb = self.sidebar(wid, ws)
            if wid != first_ch['workspace']:
                sb = sb.replace('<div data-ws="%s">' % wid, '<div data-ws="%s" style="display:none">' % wid, 1)
            sidebars.append(sb)
        b = self.book
        prologue = ['<div class="prologue">', '<h1>%s</h1>' % esc(b['title'])]
        prologue += ['<p>%s</p>' % prose(p) for p in b.get('intro', [])]
        editions = b.get('editions', [])
        if editions:
            # the other editions, linked at the end of the intro
            prologue.append('<p class="editions">%s</p>' % ' · '.join(
                '<a href="%s" hreflang="%s" lang="%s" data-lang="%s">%s</a>'
                % (attr(e['href']), attr(e['lang']), attr(e['lang']), attr(e['lang']), esc(e['label']))
                for e in editions))
        if b.get('disclaimer'):
            prologue.append('<p class="disclaimer">%s</p>' % prose(b['disclaimer']))
        prologue.append('</div>')
        head = ''
        if editions:
            config = dict(editions={e['lang']: e['href'] for e in editions},
                          detect=bool(b.get('detect_language')))
            head = '<script>var EDITIONS = %s;\n%s</script>' % (
                json.dumps(config).replace('</', '<\\/'), tpl('lang.js'))
        values = {
            'lang': attr(b['lang']),
            'head': head,
            'page_title': esc(b['page_title']),
            'style': tpl('style.css') + '\n' + self.avatars_css(),
            'workspace': esc(data['workspaces'][first_ch['workspace']]),
            'sidebars': '\n'.join(sidebars),
            'title': first_ch['title'],
            'topic': esc(first['topic']),
            'members': '<span class="avs">%s</span><span class="n">%d</span>'
                       % (''.join('<span class="mini-av av-%s"></span>' % m for m in first['avatars']), first['count']),
            'members_class': ' many' if first['many'] else '',
            'first_chapter': esc(self.first_chapter),
            'prologue': '\n'.join(prologue),
            'feed': '\n'.join(self.out),
            'epilogue': prose(b.get('epilogue', '')),
            # "</" cannot appear inside a <script> element
            'scenes': json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'),
            'script': tpl('app.js'),
        }
        return re.sub(r'\{\{(\w+)\}\}', lambda m: values[m.group(1)], tpl('page.html'))


def main(argv):
    out_dir = ROOT
    if len(argv) > 2 and argv[1] == '--out':
        out_dir = os.path.abspath(argv[2])
    try:
        cast = load_json(os.path.join(ROOT, 'story', 'cast.json'))
        books = sorted(glob.glob(os.path.join(ROOT, 'story', '*', 'book.json')))
        if not books:
            raise StoryError('no story/<lang>/book.json found')
        for book in books:
            ed = Edition(book, cast)
            page = ed.build()
            dest = os.path.join(out_dir, ed.book['output'])
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(page)
            print('%s: %d messages, %d chapters, %d scenes -> %s (%d KB)'
                  % (ed.book['lang'], ed.stats['messages'], ed.stats['chapters'], len(ed.scenes),
                     os.path.relpath(dest, ROOT), len(page.encode()) // 1024))
    except StoryError as e:
        print('error: %s' % e, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
