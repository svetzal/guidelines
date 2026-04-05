# Slidev Animations Reference

Click animations, motion, and slide transitions.

## v-click

Makes elements appear incrementally on click. Three forms:

### Component Form

```html
<v-click>

This paragraph appears on click.

</v-click>
```

### Directive Form

```html
<div v-click>Appears on click</div>
```

### On Lists (v-clicks)

Applies click animation to each child element:

```html
<v-clicks>

- First point (click 1)
- Second point (click 2)
- Third point (click 3)

</v-clicks>
```

**Props:**

| Prop | Default | Description |
|------|---------|-------------|
| `depth` | 1 | Depth of nested lists to animate |
| `every` | 1 | Items revealed per click |

```html
<!-- Animate nested lists too -->
<v-clicks depth="2">

- Parent item (click 1)
  - Child item (click 2)
  - Child item (click 3)
- Parent item (click 4)

</v-clicks>

<!-- Reveal 2 items at a time -->
<v-clicks every="2">

- Item A (click 1)
- Item B (click 1)
- Item C (click 2)
- Item D (click 2)

</v-clicks>
```

## v-after

Element appears at the same click as the previous v-click. Shorthand for `v-click="'+0'"`.

```html
<div v-click>First (click 1)</div>
<div v-after>Also first (click 1)</div>
<div v-click>Second (click 2)</div>
```

## Hide Modifier

Makes elements disappear on click instead of appearing:

```html
<div v-click.hide>Visible initially, hidden on click</div>
<v-click hide>Also hides</v-click>
```

## Click Positioning

### Relative Positioning (default)

Click order is calculated relative to previous elements:

```html
<div v-click>Click 1 (default: '+1')</div>
<div v-click="'+2'">Click 3 (skips one)</div>
<div v-click="'+0'">Click 3 (same as previous, like v-after)</div>
```

### Absolute Positioning

Specify exact click number:

```html
<div v-click="3">Appears at exactly click 3</div>
<div v-click="1">Appears at exactly click 1</div>
```

### Enter & Leave Ranges

Control when an element appears and disappears:

```html
<!-- Visible from click 2 to click 4 -->
<div v-click="[2, 5]">Visible at clicks 2, 3, 4</div>
```

## VSwitch Component

Toggle between content on clicks:

```html
<v-switch>
  <template #1>Shown at click 1</template>
  <template #2>Shown at click 2</template>
  <template #3>Shown at click 3</template>
</v-switch>
```

## v-motion

Animate element properties across click states.

### Basic Motion

```html
<div
  v-motion
  :initial="{ x: -80, opacity: 0 }"
  :enter="{ x: 0, opacity: 1 }">
  Slides in from left on enter
</div>
```

### Click-Triggered Motion

```html
<div
  v-motion
  :initial="{ x: -80 }"
  :enter="{ x: 0 }"
  :click-1="{ x: 100 }"
  :click-2="{ x: 200, scale: 1.2 }"
  :leave="{ x: 300, opacity: 0 }">
  Moves right on each click
</div>
```

### Motion Variants

| Variant | When Applied |
|---------|-------------|
| `initial` | Before slide enters |
| `enter` | When slide becomes active |
| `click-N` | At click number N |
| `click-N-M` | From click N through click M |
| `leave` | When slide transitions out |

### Animatable Properties

`x`, `y`, `scale`, `scaleX`, `scaleY`, `rotate`, `rotateX`, `rotateY`, `rotateZ`, `skewX`, `skewY`, `opacity`

## Slide Transitions

Set in headmatter (global) or per-slide frontmatter.

### Built-in Transitions

| Transition | Effect |
|------------|--------|
| `fade` | Fade in/out |
| `fade-out` | Fade out then in |
| `slide-left` | Slide from right to left |
| `slide-right` | Slide from left to right |
| `slide-up` | Slide from bottom to top |
| `slide-down` | Slide from top to bottom |
| `view-transition` | Uses View Transitions API (experimental) |

### Global Default

```yaml
---
transition: slide-left
---
```

### Per-Slide Override

```yaml
---
transition: fade
---

# This Slide Fades
```

### Forward/Backward Variants

Different transitions for forward and backward navigation:

```yaml
---
transition: slide-left | slide-right
---
```

Format: `forward-transition | backward-transition`

### Custom Transitions

Define custom CSS transitions:

```yaml
---
transition: my-transition
---
```

```css
/* In <style> block or global styles */
.my-transition-enter-active,
.my-transition-leave-active {
  transition: all 0.5s ease;
}
.my-transition-enter-from {
  opacity: 0;
  transform: translateX(50px);
}
.my-transition-leave-to {
  opacity: 0;
  transform: translateX(-50px);
}
```

## Default Click Styling

Elements targeted by v-click get these CSS classes:

- `slidev-vclick-target` — always present on v-click elements
- `slidev-vclick-hidden` — when element is hidden (before its click)

Override the default fade transition:

```css
.slidev-vclick-target {
  transition: all 0.5s ease;
}
.slidev-vclick-hidden {
  opacity: 0;
  transform: scale(0.8);
}
```
