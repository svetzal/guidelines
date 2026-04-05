# Template: Blog Post Conversion (10-25 slides)

Use this template when converting an existing blog post into a slide presentation.
The comments guide the conversion process — replace all `[PLACEHOLDER]` values.

## Conversion Principles

- **Distill, don't transcribe** — slides are not the blog post on screen
- **One idea per slide** — each blog paragraph may become 1-3 slides
- **Speaker notes carry depth** — put the original prose in notes, bullet points on slides
- **Preserve the voice** — rhetorical questions, humor, and anecdotes are the best parts

---

```markdown
---
theme: default
title: "[POST TITLE]"
author: "Stacey Vetzal"
info: |
  Based on the blog post "[Post Title]"
  by Stacey Vetzal.
transition: slide-left
---

# [POST TITLE]

[Subtitle derived from the post's central question or thesis]

<div class="absolute bottom-10 left-12 text-sm opacity-60">
Stacey Vetzal
</div>

<!--
FROM POST: The title and opening paragraph.
This cover slide uses the post title directly.
The subtitle should capture the post's core question.
-->

---
layout: center
---

# [HOOK FROM OPENING ANECDOTE]

<!--
FROM POST: The opening anecdote or vignette.
Distill it to the most vivid sentence or question.
Tell the full story in your notes.
-->

---

## [OPENING ANECDOTE — KEY MOMENT]

[2-3 sentences capturing the heart of the story]

<!--
FROM POST: Opening anecdote paragraphs.
Put the full original text here in notes for reference while presenting.
On the slide, keep only the essence — the moment that makes people nod.
-->

---
layout: section
---

# [H2 SECTION 1 FROM POST]

<!--
FROM POST: First H2 heading.
Each major section of the blog post becomes a section divider + content slides.
-->

---

## [KEY POINT FROM SECTION 1]

<v-clicks>

- [Distilled from paragraph 1]
- [Distilled from paragraph 2]
- [Distilled from paragraph 3]

</v-clicks>

<!--
FROM POST: The body paragraphs of section 1.
DISTILLATION: Each paragraph → one bullet point capturing its core claim.
Original text preserved here in notes for the speaker.
-->

---
layout: quote
---

# "[RHETORICAL QUESTION FROM POST]"

<!--
FROM POST: A rhetorical question that appeared in the blog post.
These translate beautifully to full-screen statement slides.
Pause and let the audience sit with it.
-->

---

## [CONTINUED SECTION 1 CONTENT]

<v-clicks>

- [Additional point]
- [Additional point]

</v-clicks>

<!--
FROM POST: More content from the same section, if it needs multiple slides.
Rule of thumb: if you have more than 4 bullets, split into two slides.
-->

---
layout: section
---

# [H2 SECTION 2 FROM POST]

---

## [KEY POINT FROM SECTION 2]

<v-clicks>

- [Distilled point]
- [Distilled point]
- [Distilled point]

</v-clicks>

<!--
FROM POST: Section 2 content.
Same distillation approach — one clear point per bullet.
-->

---
layout: two-cols
---

## [COMPARISON FROM POST]

<v-clicks>

- [Side A point 1]
- [Side A point 2]

</v-clicks>

::right::

## [VS]

<v-clicks>

- [Side B point 1]
- [Side B point 2]

</v-clicks>

<!--
FROM POST: If the blog post compares two ideas, approaches, or scenarios,
use a two-column layout. Analogies also work well here.
-->

---

## [CODE EXAMPLE FROM POST]

<!-- Keep only the essential lines — trim setup/boilerplate -->

```ts {1|3-5}
// [What this demonstrates]
const before = '[original approach]'

function improved(input: string) {
  return '[better approach]'
}
```

<!--
FROM POST: Code block.
DISTILLATION: Trim to max 12-15 lines. Remove boilerplate.
Highlight the lines that matter with click-stepped reveals.
-->

---
layout: section
---

# [H2 SECTION 3 FROM POST]

---

## [KEY INSIGHT FROM SECTION 3]

<v-clicks>

- [Point]
- [Point]
- [Point]

</v-clicks>

<!--
FROM POST: This is often where the post's deepest insight lives.
Give it room to breathe — don't rush past it.
-->

---

## [ANALOGY OR MICRO-STORY FROM POST]

[The vivid comparison or secondary story, distilled to 2-3 lines]

<!--
FROM POST: Analogies and micro-stories are gold for presentations.
Keep the punchline on the slide. Full context in notes.
-->

---
layout: statement
---

# [POST'S CLOSING INSIGHT]

<!--
FROM POST: The closing paragraph.
Distill to one sentence — the thing you want people to carry away.
Blog posts often end with a call to reflection or hopeful reframing.
-->

---
layout: end
---

# Thank You

[Contact info / blog URL]

<!--
Link back to the original blog post for people who want to read more.
-->
```

## Conversion Mapping Guide

Use this table format when planning the conversion:

| Post Element | Slide # | Layout | Conversion Notes |
|-------------|---------|--------|-----------------|
| Title | 1 | cover | Post title + subtitle from thesis |
| Opening anecdote | 2-3 | center, default | Distill to hook + key moment |
| H2: [Section] | 4 | section | Section divider |
| Paragraphs | 5-6 | default | One idea per slide, v-clicks |
| Rhetorical Q | 7 | quote | Full-screen statement |
| H2: [Section] | 8 | section | Section divider |
| Comparison | 9 | two-cols | Side-by-side |
| Code block | 10 | default | Trim + highlight |
| H2: [Section] | 11 | section | Section divider |
| Key insight | 12 | default | Progressive reveal |
| Analogy | 13 | default | Keep punchline |
| Closing | 14 | statement | One sentence |
| End | 15 | end | Thank you + link |
