# Slidev Components Reference

Built-in components, custom components, and global layers.

## Visual & Layout Components

### Arrow

Draws an SVG arrow between two points.

```html
<Arrow x1="10" y1="20" x2="200" y2="100" />
```

| Prop | Type | Description |
|------|------|-------------|
| `x1` | number | Start X coordinate |
| `y1` | number | Start Y coordinate |
| `x2` | number | End X coordinate |
| `y2` | number | End Y coordinate |
| `width` | number | Line width (default: 2) |
| `color` | string | Line color |
| `two-way` | boolean | Draw arrow on both ends |

### VDragArrow

Draggable arrow — same props as Arrow but can be repositioned in dev mode.

### AutoFitText

Text that automatically resizes to fit its container.

```html
<AutoFitText :max="200" :min="50" modelValue="Big Text" />
```

### Transform

Apply CSS transforms to child content.

```html
<Transform :scale="0.5">
  <p>This is 50% size</p>
</Transform>
```

## Navigation Components

### Link

Navigate to a specific slide.

```html
<Link to="5">Go to slide 5</Link>
<Link to="my-slide-name">Go to named slide</Link>
```

### Toc (Table of Contents)

Generates a table of contents from slide headings.

```html
<Toc />
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `columns` | number | 1 | Number of columns |
| `maxDepth` | number | Infinity | Max heading depth |
| `minDepth` | number | 1 | Min heading depth |
| `mode` | string | 'all' | Filter mode: 'all', 'onlyCurrentTree', 'onlySiblings' |
| `listClass` | string | '' | CSS class for the list |

```html
<!-- Two-column TOC, only h1 and h2 -->
<Toc columns="2" :maxDepth="2" />
```

### TitleRenderer

Renders the title of a specific slide.

```html
<TitleRenderer no="5" />
```

### SlideCurrentNo / SlidesTotal

Display current slide number or total count.

```html
Slide <SlideCurrentNo /> of <SlidesTotal />
```

## Conditional Rendering

### LightOrDark

Show different content based on light/dark mode.

```html
<LightOrDark>
  <template #dark>
    <img src="/dark-logo.png" />
  </template>
  <template #light>
    <img src="/light-logo.png" />
  </template>
</LightOrDark>
```

### RenderWhen

Render content only in specific contexts.

```html
<RenderWhen context="presenter">
  Only visible in presenter view
</RenderWhen>

<RenderWhen context="slide">
  <template #fallback>
    Fallback content for other contexts
  </template>
  Only in slide view
</RenderWhen>
```

Contexts: `'slide'`, `'overview'`, `'presenter'`, `'preparser'`

## Media Components

### Tweet

Embed a tweet by ID.

```html
<Tweet id="1390115482657726468" />
```

| Prop | Type | Description |
|------|------|-------------|
| `id` | string | Tweet ID |
| `scale` | number | Scale factor (default: 1) |
| `conversation` | string | Show conversation: 'none' to hide |
| `cards` | string | Show cards: 'hidden' to hide |

### Youtube

Embed a YouTube video.

```html
<Youtube id="luoMHjh-XcQ" />
```

| Prop | Type | Description |
|------|------|-------------|
| `id` | string | YouTube video ID |
| `width` | number | Width in px (default: 480) |
| `height` | number | Height in px (default: 270) |

### SlidevVideo

Custom video player with presentation-friendly controls.

```html
<SlidevVideo v-click autoplay>
  <source src="/video.mp4" type="video/mp4" />
</SlidevVideo>
```

| Prop | Type | Description |
|------|------|-------------|
| `controls` | boolean | Show controls |
| `autoplay` | boolean | Auto-play when slide is active |
| `autoreset` | string | Reset on slide change: 'slide', 'click' |
| `poster` | string | Poster image URL |
| `timestamp` | string | Start timestamp |

## Interactive Components

### VDrag

Make any element draggable in dev mode. Positions persist.

```html
<v-drag>
  <div class="bg-blue-500 p-4 rounded">
    Drag me around!
  </div>
</v-drag>
```

### VSwitch

Toggle between content on clicks.

```html
<v-switch>
  <template #1>Step 1 content</template>
  <template #2>Step 2 content</template>
  <template #3>Step 3 content</template>
</v-switch>
```

| Prop | Type | Description |
|------|------|-------------|
| `unmount` | boolean | Unmount hidden slots (default: false) |
| `tag` | string | Wrapper element tag |
| `transition` | object | Transition config |

## Utility Components

### PoweredBySlidev

Attribution badge linking to Slidev.

```html
<PoweredBySlidev />
```

## Custom Components

Create custom Vue components in the `components/` directory:

```
presentations/my-talk/
├── slides.md
└── components/
    └── Counter.vue
```

```vue
<!-- components/Counter.vue -->
<template>
  <div class="p-4">
    <button @click="count++">Count: {{ count }}</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>
```

Use in slides:

```html
<Counter />
```

Components are auto-imported — no import statement needed.

## Global Layers

Special components that appear on every slide:

| File | Position | Description |
|------|----------|-------------|
| `global-top.vue` | Above all slides | Persistent overlay (e.g., logo) |
| `global-bottom.vue` | Below all slides | Persistent underlay (e.g., watermark) |
| `slide-top.vue` | Top of each slide | Per-slide header area |
| `slide-bottom.vue` | Bottom of each slide | Per-slide footer area |

Place in the presentation root alongside `slides.md`.

```vue
<!-- global-bottom.vue -->
<template>
  <div class="absolute bottom-2 right-4 text-xs opacity-50">
    Stacey Vetzal — {{ $slidev.nav.currentPage }}/{{ $slidev.nav.total }}
  </div>
</template>
```
