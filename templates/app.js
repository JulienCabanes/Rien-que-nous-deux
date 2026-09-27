// Scenes: the header and sidebar follow the channel being read.
// build.py tags an element with data-scene="N" wherever the scene changes
// (channel switch, member joining or leaving, topic change) and embeds the
// scene list in #scenes. This script only displays the last scene scrolled past.
(function () {
  var data = JSON.parse(document.getElementById('scenes').textContent);
  var markers = [].slice.call(document.querySelectorAll('[data-scene]'));
  var ws = document.getElementById('wsname');
  var title = document.getElementById('hdtitle');
  var topic = document.getElementById('hdtopic');
  var members = document.getElementById('members');
  var sidebars = [].slice.call(document.querySelectorAll('.sidebar [data-ws]'));
  var current = -1;

  function apply(n) {
    current = n;
    var s = data.scenes[n], ch = data.channels[s.channel];
    ws.textContent = data.workspaces[ch.workspace];
    title.innerHTML = ch.title;
    topic.textContent = s.topic;
    members.classList.toggle('many', s.avatars.length > 7);
    members.innerHTML = '<span class="avs">' + s.avatars.map(function (id) {
      return '<span class="mini-av av-' + id + '"></span>';
    }).join('') + '</span><span class="n">' + s.count + '</span>';
    sidebars.forEach(function (sb) {
      sb.style.display = sb.getAttribute('data-ws') === ch.workspace ? '' : 'none';
      [].forEach.call(sb.querySelectorAll('[data-channel]'), function (item) {
        var on = item.getAttribute('data-channel') === s.channel;
        item.classList.toggle('active', on);
        if (item.hasAttribute('data-only-active')) item.style.display = on ? '' : 'none';
      });
    });
  }

  // A change applies once it reaches the middle of the screen.
  function check() {
    var n = 0, y = window.innerHeight / 2;
    for (var i = 0; i < markers.length; i++) {
      if (markers[i].getBoundingClientRect().top > y) break;
      n = +markers[i].getAttribute('data-scene');
    }
    if (n !== current) apply(n);
  }

  check();
  window.addEventListener('scroll', check, { passive: true });
  window.addEventListener('resize', check);
})();

// Chapter menu and reading progress bar.
(function () {
  var chaps = [].slice.call(document.querySelectorAll('.daymark'));
  var menu = document.getElementById('chapmenu');
  var btn = document.getElementById('chapbtn');
  var now = document.getElementById('chapnow');
  var bar = document.getElementById('chapbar');
  if (!chaps.length || !menu) return;
  chaps.forEach(function (c) {
    var a = document.createElement('a');
    a.href = '#' + c.id;
    a.innerHTML = c.dataset.d1 + ' <span class="m2">· ' + c.dataset.d2 + '</span>';
    a.addEventListener('click', function () { menu.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); });
    menu.appendChild(a);
  });
  btn.addEventListener('click', function () {
    var o = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
  document.addEventListener('click', function (e) {
    if (!bar.contains(e.target)) { menu.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
  });
  var prog = document.createElement('div');
  prog.className = 'progress';
  document.body.appendChild(prog);
  var links = [].slice.call(menu.children);
  function update() {
    var y = bar.getBoundingClientRect().bottom + 4, cur = 0;
    for (var i = 0; i < chaps.length; i++) if (chaps[i].getBoundingClientRect().top <= y) cur = i;
    now.textContent = chaps[cur].dataset.d1 + ' · ' + chaps[cur].dataset.d2;
    links.forEach(function (l, i) { l.classList.toggle('cur', i === cur); });
    var max = document.documentElement.scrollHeight - window.innerHeight;
    prog.style.width = (max > 0 ? (window.scrollY / max * 100) : 0) + '%';
  }
  update();
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
})();
