# Slidev Export and Deploy Reference

Exporting to PDF/PPTX/PNG and deploying as a web app.

## Prerequisites

Install Playwright for CLI export:

```bash
npm install -D playwright-chromium
```

This is only needed for export, not for development.

## Export Formats

### PDF (Default)

```bash
npx slidev export slides.md
```

Output: `./slides-export.pdf`

### PowerPoint (PPTX)

```bash
npx slidev export slides.md --format pptx
```

All slides are exported as images (text is not selectable). Presenter notes are included.

### PNG (Individual Images)

```bash
npx slidev export slides.md --format png
```

Creates one PNG file per slide (or per click step with `--with-clicks`).

### Markdown (with Embedded Images)

```bash
npx slidev export slides.md --format md
```

Compiles a single markdown file with PNG images embedded.

## Common Options

| Flag | Description |
|------|-------------|
| `--output <name>` | Output filename (default: slides-export) |
| `--with-clicks` | Export each click step as a separate page/image |
| `--range 1,6-8,10` | Export only specific slides |
| `--dark` | Export using dark mode theme |
| `--timeout 60000` | Playwright timeout in ms (increase for complex slides) |
| `--wait 10000` | Delay before export starts (ms) |
| `--wait-until <state>` | Wait condition: `networkidle` (default), `domcontentloaded`, `load`, `none` |
| `--with-toc` | Generate PDF outline/bookmarks |
| `--omit-background` | Transparent PNG backgrounds |
| `--executable-path <path>` | Custom Chrome/Edge path |

### Examples

```bash
# Export slides 1-5 and 10 as dark mode PDF
npx slidev export slides.md --range 1-5,10 --dark

# Export with click animations as separate pages
npx slidev export slides.md --with-clicks --output my-talk

# Export PNGs with longer timeout for heavy slides
npx slidev export slides.md --format png --timeout 120000

# Export all slides as individual images
npx slidev export slides.md --format png --range 1-999
```

## Headmatter Export Config

Set defaults in headmatter:

```yaml
---
exportFilename: my-talk-export     # Default output filename
download: true                     # Show download button in presentation
---
```

`download` can also be a URL string for hosting the PDF elsewhere:

```yaml
download: 'https://example.com/my-talk.pdf'
```

## Multiple Presentations

Export multiple files at once:

```bash
npx slidev export slides1.md slides2.md
npx slidev export *.md
```

## Browser UI Export

During development (`npx slidev`), access the export UI:

1. Open the presentation in a Chromium-based browser
2. Navigate to the export page via the toolbar
3. Use the browser print dialog for PDF

This avoids the playwright-chromium dependency for simple exports.

## Deployment as SPA

Build as a static single-page application:

```bash
npx slidev build slides.md
```

Output: `./dist/` directory containing a static site.

### Build Options

```bash
npx slidev build slides.md --base /talks/my-talk/  # Custom base path
npx slidev build slides.md --out ./build           # Custom output dir
```

### GitHub Pages

1. Build with base path matching your repo:

```bash
npx slidev build slides.md --base /repo-name/
```

2. Deploy the `dist/` directory to GitHub Pages.

Or use a GitHub Action:

```yaml
# .github/workflows/deploy.yml
name: Deploy Slides
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install
      - run: npx slidev build slides.md --base /${{ github.event.repository.name }}/
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

### Netlify

```bash
npx slidev build slides.md
# Deploy dist/ directory to Netlify
```

Or set up automatic deployment with a `netlify.toml`:

```toml
[build]
  command = "npx slidev build slides.md"
  publish = "dist"
```

### Vercel

```bash
npx slidev build slides.md
# Deploy dist/ directory to Vercel
```

### Docker

```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY . .
RUN npm install
RUN npx slidev build slides.md

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

## Troubleshooting

- **Missing content in export**: Use `--wait 5000` to allow animations to settle
- **Broken emojis in PDF**: Install emoji fonts (e.g., `fonts-noto-color-emoji` on Linux)
- **Timeout errors**: Increase `--timeout` for complex slides with heavy diagrams
- **Blank slides in PPTX**: Expected for slides that rely on animations — PPTX captures static state
- **Large PDF size**: Use `--range` to export only needed slides, or compress afterward
