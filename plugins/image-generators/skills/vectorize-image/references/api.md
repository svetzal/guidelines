# vectorizer.ai API reference

Full parameter list for `POST https://api.vectorizer.ai/api/v1/vectorize`.
The bundled `scripts/vectorize.py` covers the common path; reach for anything
below by passing `-P name=value` (repeatable). Auth is HTTP Basic
(`VECTORIZER_API_ID` : `VECTORIZER_API_SECRET`).

## Table of contents

- [Input](#input)
- [Mode & cost](#mode--cost)
- [Output format](#output-format)
- [Processing (colours, shapes)](#processing)
- [Output style](#output-style)
- [Curve & line fitting](#curve--line-fitting)
- [Output sizing](#output-sizing)
- [Retention & tokens](#retention--tokens)
- [Response headers](#response-headers)
- [Errors & rate limits](#errors--rate-limits)
- [Companion endpoints](#companion-endpoints)

## Input

Supply the image one way (the script picks the field for you from the input arg):

| Field | Meaning |
| ----- | ------- |
| `image` | binary file upload (multipart) |
| `image.base64` | base64 data, max 1 MB |
| `image.url` | remote URL to fetch |
| `image.token` | reuse a previously stored image |

Accepted: BMP, GIF, JPEG, PNG, TIFF, WebP. Max 33,554,432 px; downscaled to
`input.max_pixels` (default 2097252, range 100–3145828) if larger.

## Mode & cost

`mode` (default `production`):

| Mode | Credits | Output |
| ---- | ------- | ------ |
| `production` | 1.0 | clean, deliverable |
| `preview` | 0.2 | watermarked PNG, 4× size |
| `test` | 0 | heavily watermarked (pipeline checks) |
| `test_preview` | 0 | heavily watermarked preview |

## Output format

`output.file_format` (default `svg`): `svg` | `eps` | `pdf` | `dxf` | `png`

SVG: `output.svg.version` = `svg_1_0` | `svg_1_1` (default) | `svg_tiny_1_2`;
`output.svg.fixed_size` (bool); `output.svg.adobe_compatibility_mode` (bool).

DXF: `output.dxf.compatibility_level` = `lines_only` | `lines_and_arcs` (default) | `lines_arcs_and_splines`.

PNG: `output.bitmap.anti_aliasing_mode` = `anti_aliased` (default) | `aliased`.

## Processing

| Param | Range | Default | Notes |
| ----- | ----- | ------- | ----- |
| `processing.max_colors` | 0–256 | 0 | 0 = unlimited; 1–2 = binary |
| `processing.palette` | — | empty | snap/remap colours, e.g. `#FF0000;#00FF00;#0000FF;` |
| `processing.shapes.min_area_px` | 0.0–100.0 | 0.125 | discard shapes smaller than this |

## Output style

| Param | Default | Options |
| ----- | ------- | ------- |
| `output.draw_style` | `fill_shapes` | `fill_shapes` \| `stroke_shapes` \| `stroke_edges` |
| `output.shape_stacking` | `cutouts` | `cutouts` \| `stacked` |
| `output.group_by` | `none` | `none` \| `color` \| `parent` \| `layer` |
| `output.parameterized_shapes.flatten` | `false` | flatten circles/ellipses/rects/triangles/stars |

Stroke style (when `draw_style` is a stroke variant):
`output.strokes.non_scaling_stroke` (bool, default true),
`output.strokes.use_override_color` (bool), `output.strokes.override_color`
(hex, default `#000000`), `output.strokes.stroke_width` (0.0–5.0, default 1.0).

Gap filler (on by default, fixes viewer hairline artifacts):
`output.gap_filler.enabled` (true), `output.gap_filler.clip` (false),
`output.gap_filler.non_scaling_stroke` (true), `output.gap_filler.stroke_width`
(0.0–5.0, default 2.0).

## Curve & line fitting

Toggle allowed primitives (all default `true`):
`output.curves.allowed.quadratic_bezier`, `.cubic_bezier`, `.circular_arc`,
`.elliptical_arc`. Fit tolerance: `output.curves.line_fit_tolerance`
(0.001–1.0 px, default 0.1).

## Output sizing

| Param | Range | Default | Notes |
| ----- | ----- | ------- | ----- |
| `output.size.scale` | 0.0–1000.0 | — | uniform scale; overrides width/height |
| `output.size.width` | 0.0–1e12 | — | physical/pixel width |
| `output.size.height` | 0.0–1e12 | — | physical/pixel height |
| `output.size.unit` | — | `none` | `none` \| `px` \| `pt` \| `in` \| `cm` \| `mm` |
| `output.size.aspect_ratio` | — | `preserve_inset` | `preserve_inset` \| `preserve_overflow` \| `stretch` |
| `output.size.align_x` / `align_y` | 0.0–1.0 | 0.5 | 0=left/top, 1=right/bottom |
| `output.size.input_dpi` / `output_dpi` | 1.0–1e6 | — | DPI overrides |

## Retention & tokens

`policy.retention_days` (0–30, default 0): retains image+result and returns an
`X-Image-Token`. With a token you can re-vectorize or pull other formats cheaply
(pass `token:<id>` as the input). Production downloads from a preview token
return an `X-Receipt` for reduced-rate format downloads.

## Response headers

| Header | When | Meaning |
| ------ | ---- | ------- |
| `X-Credits-Charged` | always | credits actually spent |
| `X-Credits-Calculated` | test modes | what production would cost |
| `X-Image-Token` | `retention_days > 0` | reuse handle for cheap re-downloads |
| `X-Receipt` | prod from preview token | reduced-rate format downloads |

## Errors & rate limits

Errors are JSON: `{"error": {"status", "code", "message"}}` with HTTP 400–599.
The script parses and surfaces `code` + `message`. Rate limits are generous; on
HTTP 429 apply linear backoff (5s, 10s, 15s…). Idle timeout ≥ 180s; requests
normally finish in seconds.

## Companion endpoints

- `POST /api/v1/download` — fetch additional formats or upgrade a preview to
  production using an image token.
- `POST /api/v1/delete` — delete a retained image before retention expires.
- `GET /api/v1/account` — plan, state, remaining credits.
