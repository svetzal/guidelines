# Intent atlas site

A static visualization of the intent records in this repository, published to
GitHub Pages by `.github/workflows/pages.yml` on every push to `main` that
touches `intents/**` or `site/**`.

- `build.py` — stdlib-only generator (Python 3.11+). Reads
  `intents/craftsperson/*.toml`, distills each record (title, category, tags,
  confidence, capability/threat/strategy/tradeoff, the evidence criteria that
  show the intent is being honored, per-language good/bad code examples,
  ecosystem coverage from `scope.paths`), and injects the set as JSON into
  the template along with the vendored highlight.js bundle.
- `merge_examples.py` — merges per-language example fragments
  (`<lang>.json` keyed by intent slug, values `{good, bad}`) into the
  `[examples.<lang>]` tables of the intent records. Idempotent: everything
  below the marker comment in each TOML is regenerated from the merge.
- `vendor/` — pinned highlight.js 11.11.1 (BSD-3-Clause) from cdnjs:
  the common-languages bundle plus clojure and elixir grammars. Inlined
  into the page at build time so the site stays a single self-contained
  file.
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
