#!/usr/bin/env python3
"""Validateur de structure pour Rien que nous deux."""
import re
import sys
from html.parser import HTMLParser

MSG_RE = re.compile(r'<div class="msg"[^>]*>')
VOID = ('br', 'img', 'meta', 'link', 'input')


def spans(h):
    out = []
    for m in MSG_RE.finditer(h):
        depth, pos = 1, m.end()
        while depth > 0:
            o, c = h.find('<div', pos), h.find('</div>', pos)
            if c < 0:
                return out
            if 0 <= o < c:
                depth, pos = depth + 1, o + 4
            else:
                depth, pos = depth - 1, c + 6
        out.append((m.start(), pos))
    return out


def validate(h):
    class P(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack, self.errors = [], []

        def handle_starttag(self, t, a):
            if t not in VOID:
                self.stack.append((t, self.getpos()))

        def handle_endtag(self, t):
            if self.stack and self.stack[-1][0] == t:
                self.stack.pop()
            else:
                self.errors.append(('fermeture orpheline <%s>' % t, self.getpos()))

    p = P()
    p.feed(h)
    return p.errors + [('balise non fermée <%s>' % t, pos) for t, pos in p.stack]


def unbalanced(h):
    return [(s, re.sub('<[^>]+>', '', h[s:e])[:60])
            for s, e in spans(h) if h[s:e].count('<div') != h[s:e].count('</div>')]


def nested(h):
    return [(s, re.sub('<[^>]+>', '', h[s:s + 300])[:60])
            for s, e in spans(h) if '<div class="msg"' in h[s + 5:e]]


def main(path):
    h = open(path, encoding='utf-8').read()
    checks = [('structure HTML', validate(h)),
              ('messages déséquilibrés', unbalanced(h)),
              ('messages imbriqués', nested(h))]
    ko = 0
    for name, errs in checks:
        print(('  OK  ' if not errs else '  KO  ') + name + (' : %d' % len(errs) if errs else ''))
        for e in errs[:5]:
            print('        ', e)
        ko += len(errs)
    print('\n%d messages, %d chapitres' % (len(spans(h)), h.count('class="daymark"')))
    return 1 if ko else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'index.html'))
