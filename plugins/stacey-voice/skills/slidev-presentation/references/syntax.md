# Slidev Markdown Syntax Reference

Advanced markdown syntax features beyond basic slides.

## MDC Syntax (Markdown Components)

Enable with `mdc: true` in headmatter. Allows using Vue-like component syntax in markdown.

### Inline Components

```markdown
This text has :ComponentName{prop="value"} inline.
```

### Block Components

```markdown
::ComponentName{prop="value"}
Content inside the component
::
```

## Speaker Notes

HTML comments at the end of a slide become presenter notes:

```markdown
# Slide Title

Content here

<!--
Speaker notes go here.
Supports **markdown** formatting.

- Key point to mention
- Remember to pause here
-->
```

View notes by pressing `p` in dev mode to enter presenter view.

## External Slide Imports

Import slides from other files using `src` in frontmatter:

```markdown
---
src: ./shared/intro.md
---
```

Import specific slides from a file:

```markdown
---
src: ./other-deck.md
---
```

The imported file follows the same slide separator conventions. Relative paths are resolved from the importing file's location.

## Multi-File Structure

Large presentations can be split across files:

```
presentations/my-talk/
├── slides.md           # Main file, imports others
├── intro.md            # Introduction section
├── demo.md             # Demo section
└── closing.md          # Closing section
```

In `slides.md`:

```markdown
---
title: My Talk
---

# Welcome

---
src: ./intro.md
---

---
src: ./demo.md
---

---
src: ./closing.md
---
```

## Scoped Styles

Add CSS scoped to a single slide using `<style>` at the end:

```markdown
# My Slide

Content here

<style>
h1 {
  color: #2B90B6;
}
</style>
```

Styles are automatically scoped to the current slide.

## Global Styles

Apply styles across all slides:

```markdown
# Slide

<style global>
.slidev-layout h1 {
  font-size: 2.5em;
}
</style>
```

Or create a `styles/` directory in the presentation root:

```
presentations/my-talk/
├── slides.md
└── styles/
    └── index.css
```

## Context Variables

Available in markdown when using MDC syntax:

| Variable | Description |
|----------|-------------|
| `$slidev.nav.currentPage` | Current slide number |
| `$slidev.nav.total` | Total slide count |
| `$frontmatter` | Current slide's frontmatter |
| `$clicks` | Current click count on this slide |
| `$page` | Current page number |
| `$renderContext` | Render context: 'slide', 'overview', 'presenter', 'preparser' |

## Escaping

To show literal `---` without creating a slide separator, escape it:

```markdown
\---
```

To show literal Vue/MDC syntax without rendering:

```markdown
\:ComponentName
```

## HTML in Markdown

Standard HTML is supported in slide content:

```html
<div class="flex gap-4">
  <div class="flex-1">Column 1</div>
  <div class="flex-1">Column 2</div>
</div>
```

## Slot Syntax

Named slots for layouts use `::name::` syntax:

```markdown
---
layout: two-cols
---

Content in default (left) slot

::right::

Content in right slot
```

Available slots depend on the layout. See `references/layouts.md` for each layout's slots.
