# Rien que nous deux

A fiction told as a Slack conversation. The site is generated; never edit HTML
by hand.

- Story sources: `story/<lang>/*.txt` (one file per chapter), `story/<lang>/book.json`
  (UI strings, workspaces, channels), `story/cast.json` (characters).
  The format is documented in `README.md` (in French).
- Code, keywords, directives and identifiers are in English; story text is in
  the edition's language. The author writes in French.
- After any change: `python3 tools/build.py && python3 tools/check.py`
  (both must pass), then commit the regenerated `index.html` together with the
  sources. `index.html` is generated but committed: GitHub Pages serves it.
- `templates/` holds the page skeleton, CSS and JS. Scene changes (channel,
  member count, topic) are computed by `tools/build.py` and only displayed by
  `templates/app.js`.
- GitHub Pages serves `main` / root (deploy from branch).
