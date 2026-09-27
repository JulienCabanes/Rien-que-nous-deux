// Editions: remember the one a reader picks, and on the page that sets
// "detect_language" send first-time visitors to the edition their browser asks for.
// EDITIONS = { editions: { <lang>: <href>, … }, detect: true|false }
(function () {
  var here = document.documentElement.lang, eds = EDITIONS.editions, KEY = 'edition';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(l) { try { localStorage.setItem(KEY, l); } catch (e) {} }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-lang]');
    if (a) set(a.getAttribute('data-lang'));
  });
  if (!EDITIONS.detect) return;
  var want = get();
  if (!want) {
    var prefs = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < prefs.length && !want; i++) {
      var code = String(prefs[i]).slice(0, 2).toLowerCase();
      if (code === here || eds[code]) want = code;
    }
    // a browser that asks for neither language gets the first edition listed
    if (!want) for (var l in eds) { want = l; break; }
  }
  if (want && want !== here && eds[want]) location.replace(eds[want] + location.hash);
})();
