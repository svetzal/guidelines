# Intent atlas site

A static visualization of the intent records in this repository, published to
GitHub Pages by `.github/workflows/pages.yml` on every push to `main` that
touches `intents/**` or `site/**`.

- `build.py` — stdlib-only generator (Python 3.11+). Reads every generalized
  and ecosystem-specific craftsperson intent, validates relationship targets,
  distills the catalogue fields, and injects the set as JSON into the template
  along with the vendored highlight.js bundle.
- `enrich_intents.py` — deterministic editorial classification for ecosystem
  records. It adds or refreshes each record's category, topical/tool tags, and
  explicit specialization edge. Run it after adding or renaming ecosystem
  intents and review the resulting taxonomy changes.
- The catalogue's **Target language** control (also `?lang=<key>`, persisted
  across visits) drives the whole page: every general record's example pair
  renders in that language with syntax highlighting, and specialization
  records are scoped to the matching nested realization collections under
  `intents/craftsperson/`. Following a relation into another ecosystem's record
  switches the target language.
- `merge_examples.py` — merges per-language example fragments
  (`<lang>.json` keyed by intent slug, values `{good, bad}`) into the
  `[examples.<lang>]` tables of the intent records. Idempotent: everything
  below the marker comment in each TOML is regenerated from the merge.
- `vendor/` — pinned highlight.js 11.11.1 (BSD-3-Clause) from cdnjs:
  the common-languages bundle plus clojure and elixir grammars. Inlined
  into the page at build time so the site stays a single self-contained
  file. Also includes D3 7.9.0 (ISC) for force simulation, SVG selection,
  dragging, and zooming.
- `template.html` — the atlas page: a full-screen force-directed relationship
  field rendered as labelled SVG elements with pan, zoom, drag, focus, and
  progressive ecosystem disclosure. A resizable, independently scrolling
  navigator stays synchronized with the graph: categories lead to generalized
  intents, specialization parents form a visible hierarchy, relationship links
  continue the traversal, and the selected record exposes the complete claim,
  evidence, and examples. Fully self-contained (inline CSS/JS, no external
  requests), responsive, and available in light and dark themes. The
  `/*__DATA__*/` and `__BUILT__` markers are replaced at build time.
- Output lands in `_site/` (gitignored).

Build locally:

```bash
python3.11 site/build.py
open _site/index.html
```
