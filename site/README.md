# Intent atlas site

A static visualization of the intent records in this repository, published to
GitHub Pages by `.github/workflows/pages.yml` on every push to `main` that
touches `intents/**` or `site/**`.

- `build.py` — stdlib-only generator (Python 3.11+). Reads
  `intents/craftsperson/*.toml`, distills each record (title, category, tags,
  confidence, capability/threat/strategy/tradeoff, the evidence criteria that
  show the intent is being honored, ecosystem coverage from `scope.paths`),
  and injects the set as JSON into the template.
- `template.html` — the atlas page: an interactive radial map of every intent
  grouped by category, backed by expandable per-intent record cards. Fully
  self-contained (inline CSS/JS, system font stacks, no external requests),
  light and dark themes. The `/*__DATA__*/` and `__BUILT__` markers are
  replaced at build time.
- Output lands in `_site/` (gitignored).

Build locally:

```bash
python3 site/build.py
open _site/index.html
```
