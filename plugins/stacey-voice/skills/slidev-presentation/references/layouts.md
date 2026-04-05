# Slidev Layouts Reference

All built-in layouts and how to use them. Set via `layout:` in slide frontmatter.

## Basic Layouts

### `default`

Standard content layout. No special formatting.

```markdown
---
layout: default
---

# Heading

Regular content with bullets, code, etc.
```

### `center`

Centers all content vertically and horizontally.

```markdown
---
layout: center
---

# This is Centered

Great for single-statement slides.
```

### `full`

Uses the entire screen area with no padding.

### `none`

No styling at all. Blank canvas for fully custom layouts.

## Presentation Layouts

### `cover`

Title/cover slide. Typically used for the first slide (set automatically by headmatter `layout: cover`).

```markdown
---
layout: cover
background: /images/cover.png
---

# Presentation Title

Subtitle or author info
```

### `intro`

Introduction slide with title, description, and author.

### `section`

Section divider to mark the start of a new topic.

```markdown
---
layout: section
---

# Part 2: Testing
```

### `end`

Final slide of the presentation.

```markdown
---
layout: end
---

# Thank You

Questions?
```

## Content-Focused Layouts

### `fact`

Displays a single fact or data point prominently.

```markdown
---
layout: fact
---

# 73%

of developers who write tests report higher confidence in deployments
```

### `quote`

Displays a quotation with emphasis styling.

```markdown
---
layout: quote
---

# "Code is read far more often than it is written."

— Guido van Rossum
```

### `statement`

Bold assertion as the main content.

```markdown
---
layout: statement
---

# Tests are documentation that never goes stale.
```

## Two-Column Layouts

### `two-cols`

Splits content into left and right columns using the `::right::` slot separator.

```markdown
---
layout: two-cols
---

# Before

```python
def add(a, b):
    return a + b
```

::right::

# After

```python
def add(a: int, b: int) -> int:
    return a + b
```

### `two-cols-header`

Header spanning full width, then two columns below using `::left::` and `::right::`.

```markdown
---
layout: two-cols-header
---

# Comparison

::left::

## Approach A

- Simple
- Fast

::right::

## Approach B

- Flexible
- Scalable
```

## Image Layouts

### `image`

Full-screen image as the slide background.

```markdown
---
layout: image
image: /images/photo.png
backgroundSize: cover
---
```

Prop: `backgroundSize` — CSS value, default `cover`. Use `contain` to show full image.

### `image-left`

Image on the left, content on the right.

```markdown
---
layout: image-left
image: /images/diagram.png
class: my-cool-class
---

# Explanation

Content appears on the right side.
```

### `image-right`

Image on the right, content on the left.

```markdown
---
layout: image-right
image: /images/screenshot.png
---

# What You're Seeing

Explanation on the left side.
```

## Iframe Layouts

### `iframe`

Embeds a web page full-screen.

```markdown
---
layout: iframe
url: https://sli.dev
---
```

### `iframe-left` / `iframe-right`

Embedded web page on one side, content on the other.

```markdown
---
layout: iframe-right
url: https://example.com
---

# Live Demo

Check out the embedded site.
```

## Custom Layouts

Create custom layouts in `components/` or `layouts/` directory:

```
presentations/my-talk/
└── layouts/
    └── my-layout.vue
```

Reference with `layout: my-layout` in frontmatter. Custom layouts are standard Vue components that receive the slide content as a default slot.
