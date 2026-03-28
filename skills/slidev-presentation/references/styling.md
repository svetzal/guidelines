# Slidev Styling Reference

UnoCSS utilities, scoped styles, dark mode, fonts, and theme customization.

## UnoCSS Utilities

Slidev uses [UnoCSS](https://unocss.dev/) (a Tailwind-compatible utility engine). Apply classes directly in HTML or markdown.

### Common Utilities

**Text:**

```html
<div class="text-3xl font-bold text-blue-500">Large bold blue text</div>
<div class="text-sm text-gray-400 italic">Small gray italic</div>
<div class="text-center">Centered text</div>
```

**Spacing:**

```html
<div class="mt-8 mb-4 px-6">Margin top 8, bottom 4, padding x 6</div>
<div class="p-4">Padding 4 on all sides</div>
```

**Layout:**

```html
<div class="flex gap-4 items-center">
  <div class="flex-1">Column 1</div>
  <div class="flex-1">Column 2</div>
</div>

<div class="grid grid-cols-3 gap-4">
  <div>Cell 1</div>
  <div>Cell 2</div>
  <div>Cell 3</div>
</div>
```

**Background & Border:**

```html
<div class="bg-gray-100 rounded-lg shadow-lg p-4">Card style</div>
<div class="border border-gray-300 rounded p-2">Bordered box</div>
```

**Opacity & Visibility:**

```html
<div class="opacity-50">Semi-transparent</div>
<div class="invisible">Hidden but takes space</div>
```

**Position:**

```html
<div class="absolute top-4 right-4">Top right corner</div>
<div class="relative">
  <div class="absolute bottom-0 left-0">Bottom left</div>
</div>
```

### Attributify Mode

UnoCSS attributify lets you use utilities as HTML attributes:

```html
<div text="3xl blue-500" font="bold" m="t-8 b-4">
  Styled with attributes
</div>
```

## Scoped Styles

CSS scoped to a single slide. Place `<style>` at the end of the slide:

```markdown
# My Slide

Content here

<style>
h1 {
  background: linear-gradient(to right, #1e3a5f, #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
```

Styles are automatically scoped — they won't leak to other slides.

## Global Styles

Styles that apply to all slides:

### Inline Global

```markdown
<style global>
.slidev-layout h1 {
  font-size: 2.5em;
}
</style>
```

### External Stylesheet

Create `style.css` in the presentation root:

```
presentations/my-talk/
├── slides.md
└── style.css
```

This file is automatically loaded.

## Dark Mode

### Color Schema Setting

```yaml
# In headmatter
colorSchema: auto    # 'auto' | 'light' | 'dark'
```

- `auto` — follows system preference and allows toggling
- `light` — forces light mode
- `dark` — forces dark mode

### Dark-Specific Styles

Use `dark:` prefix with UnoCSS:

```html
<div class="bg-white dark:bg-gray-800 text-black dark:text-white">
  Adapts to light/dark mode
</div>
```

### LightOrDark Component

Render entirely different content per mode:

```html
<LightOrDark>
  <template #light>
    <img src="/diagram-light.png" />
  </template>
  <template #dark>
    <img src="/diagram-dark.png" />
  </template>
</LightOrDark>
```

### CSS Variables

Override theme colors in styles:

```css
:root {
  --slidev-theme-primary: #2B90B6;
  --slidev-theme-cover-background: #1a1a2e;
}
```

## Fonts

Configure in headmatter:

```yaml
fonts:
  sans: Inter              # Primary font
  serif: Merriweather      # Serif font
  mono: Fira Code          # Code font
  weights: '400,600,700'   # Font weights to load
  provider: google         # 'google' | 'none'
```

When `provider: google`, fonts are loaded from Google Fonts automatically.

Use `provider: none` if fonts are installed locally or loaded via CSS.

### Font Utilities

```html
<div class="font-sans">Sans-serif text</div>
<div class="font-serif">Serif text</div>
<div class="font-mono">Monospace text</div>
```

## Theme CSS Variables

Common variables provided by themes:

| Variable | Description |
|----------|-------------|
| `--slidev-theme-primary` | Primary accent color |
| `--slidev-theme-background` | Slide background |
| `--slidev-theme-code-background` | Code block background |
| `--slidev-theme-cover-background` | Cover slide background |
| `--slidev-theme-border` | Border color |

Override in `style.css` or a `<style global>` block.

## Useful Patterns

### Gradient Text

```html
<h1 class="bg-gradient-to-r from-blue-500 to-cyan-400 bg-clip-text text-transparent">
  Gradient Heading
</h1>
```

### Card Grid

```html
<div class="grid grid-cols-2 gap-4 mt-4">
  <div class="bg-gray-100 dark:bg-gray-800 rounded-lg p-4">
    <h3 class="font-bold">Card 1</h3>
    <p class="text-sm">Description</p>
  </div>
  <div class="bg-gray-100 dark:bg-gray-800 rounded-lg p-4">
    <h3 class="font-bold">Card 2</h3>
    <p class="text-sm">Description</p>
  </div>
</div>
```

### Full-Bleed Background with Overlay

```markdown
---
background: /images/photo.jpg
class: text-white
---

<div class="absolute inset-0 bg-black/50" />

<div class="relative z-10">

# Title Over Image

Readable text on a semi-transparent overlay

</div>
```
