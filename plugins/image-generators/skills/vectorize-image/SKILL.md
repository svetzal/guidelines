---
name: vectorize-image
description: Convert a bitmap/raster image (PNG, JPEG, GIF, BMP, TIFF, WebP) into a clean vector file (SVG, PDF, EPS, DXF, or PNG) using the vectorizer.ai API. Use this skill whenever the user wants to vectorize an image, trace a logo, turn a PNG/JPG into an SVG, get a scalable version of a raster graphic, clean up a pixelated logo, prep artwork for print or large-format display, or asks to "convert this to SVG/vector". Trigger even if they don't say "vectorize" — e.g. "make this logo scalable", "I need an SVG of this icon", "trace this bitmap", or "turn this screenshot of a logo into something crisp". Spends vectorizer.ai credits (1 per production render), so it also covers free test renders and cost-aware previews.
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
compatibility: Requires python3, network access, and VECTORIZER_API_ID / VECTORIZER_API_SECRET environment variables (a vectorizer.ai API subscription is needed for paid production/preview renders; test mode is free).
---

# Vectorize a bitmap image

Convert raster images into vector graphics through the vectorizer.ai API. The
bundled script handles auth, upload, the multipart request, error parsing, and
cost reporting. You drive it; you don't need to hand-write curl or build the
request yourself.

## Setup

The API uses HTTP Basic auth. Provide two environment variables — the
vectorizer.ai **API Id** (username) and **API Secret** (password):

```bash
export VECTORIZER_API_ID="..."
export VECTORIZER_API_SECRET="..."
```

Keep these in your shell secrets file (e.g. `~/.secrets.sh`) and source it
before running. If either is missing, the script exits with a clear message —
tell the user to add them rather than trying to discover keys elsewhere. Find
them under **Account → API** at <https://vectorizer.ai>.

## Quick start

The default produces a clean, deliverable SVG and **spends 1 credit** — that's
almost always what's wanted, so just do it:

```bash
python3 .claude/skills/vectorize-image/scripts/vectorize.py \
  /path/to/logo.png -o /path/to/logo.svg
```

The script prints the output path, bytes written, and `credits charged` so the
cost is always visible after the fact.

## Cost tiers — know what you're spending

vectorizer.ai is metered. The script's `--mode` controls the trade-off:

| `--mode` | Credits | Result | When |
| -------- | ------- | ------ | ---- |
| `production` (default) | 1.0 | clean, usable | the real deliverable |
| `preview` | 0.2 | watermarked PNG, 4× | cheap "is this trace any good?" check |
| `test` | 0 | heavy watermark | verifying the pipeline works, no charge |

Default behaviour is **production without asking** — that's usually the intent.
Drop to `--mode test` only when explicitly checking the plumbing (e.g.
confirming credentials work) so you don't burn credits on a throwaway.

**Account gate:** `production` and `preview` require a vectorizer.ai *API*
subscription — distinct from a regular subscription. Without it the API returns
HTTP 402 / code 1008 ("you need to have an API subscription…"); `test` mode
still works. That's an account/billing state, not a bug — relay the message and
point the user at <https://vectorizer.ai/pricing>; don't retry production.

## Inputs and formats

The input argument is flexible — the script figures out the source type:

- **Local file**: `logo.png` → uploaded directly. Accepts PNG, JPEG, GIF, BMP,
  TIFF, WebP.
- **Remote URL**: `https://example.com/logo.png` → fetched by the API.
- **Stored token**: `token:abc123` → reuse a previously retained image for a
  cheap re-download in another format.

Output format via `--format` (default `svg`): `svg` | `pdf` | `eps` | `dxf` |
`png`. Pick `svg` for web/most uses, `pdf`/`eps` for print workflows, `dxf` for
CAD/cutting.

```bash
# Same trace, delivered as PDF
python3 .claude/skills/vectorize-image/scripts/vectorize.py \
  poster.jpg -o poster.pdf --format pdf
```

## Tuning the trace

Most images need nothing beyond the defaults. When the user wants control, pass
any API parameter through with `-P name=value` (repeatable). The common ones:

```bash
# Flat logo with a limited palette — cap colours to keep it crisp
python3 .claude/skills/vectorize-image/scripts/vectorize.py \
  logo.png -o logo.svg -P processing.max_colors=8

# Outline / line-art style instead of filled shapes
python3 .claude/skills/vectorize-image/scripts/vectorize.py \
  sketch.png -o sketch.svg -P output.draw_style=stroke_edges

# Drop tiny speckles (raise the minimum shape area)
python3 .claude/skills/vectorize-image/scripts/vectorize.py \
  scan.png -o scan.svg -P processing.shapes.min_area_px=4
```

The full parameter catalogue — colour palettes, curve fitting, sizing/DPI,
grouping, SVG version, gap filler, retention tokens, response headers, the
companion download/delete/account endpoints — is in
[`references/api.md`](references/api.md). Read it when a request needs an option
not shown above.

## After a render

The script reports `credits charged`. If the user is iterating on settings,
suggest `--mode preview` (0.2 credit) or `--mode test` (free) for the
exploratory rounds, then one final `production` render — that's the
cost-efficient pattern. If they expect to pull multiple formats of the same
image, mention `-P policy.retention_days=N`, which returns a reusable image
token (shown in the output) so later format downloads are discounted.

## Reporting back

Confirm the output path and state the credits spent plainly (e.g. "Wrote
logo.svg — charged 1.0 credit"). If vectorizer.ai returns an error, the script
surfaces the API's `code` and `message`; relay that rather than guessing at the
cause.
