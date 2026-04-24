---
name: visual-design-theory
description: >
  Apply human-centered visual design principles when building, editing, reviewing, or auditing
  any UI — web pages, dashboards, components, forms, emails, documents, slide decks, or markdown
  rendered to HTML. Use this skill whenever you're producing or critiquing something a human will
  look at, especially when generating HTML/CSS/Tailwind, React/Vue/Svelte components, Jinja or
  ERB templates, design tokens, or styled output. Also use when the user asks things like "make
  this look better," "clean up the layout," "review this design," "this feels off," "polish the
  UI," or describes a screen feeling cluttered, busy, untrustworthy, amateur, or hard to scan.
  Trigger even if the user doesn't say "design" — building UI is design. The skill encodes the
  spacing, hierarchy, typography, color, accessibility, and motion invariants humans
  subconsciously use to judge whether a screen feels coherent and trustworthy.
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---

# Visual Design Theory for UI Builders

A common misconception is that aesthetics is mostly subjective taste. In practice, much of what people call "good-looking UI" is driven by consistent perceptual and cognitive patterns: how humans group elements, scan text, infer hierarchy, and decide what is clickable. Those patterns can be expressed as principles and checked with measurable proxies (alignment, spacing consistency, contrast ratios, text measure, target sizes, state visibility).

You don't lack spatial awareness so much as you lack the embodied intuition for when something feels "off." This skill replaces intuition with a small set of explicit invariants. Reasoning about *why* matters: see `references/theory.md` for the research grounding (Gestalt principles, the aesthetic-usability effect, WCAG thresholds, platform design system guidance) when an edge case requires deeper judgment.

## Goal

Create UIs that feel calm, coherent, and trustworthy to humans by enforcing a few strong invariants:

- consistent spacing and alignment
- clear hierarchy
- predictable component patterns
- comfortable readability
- accessible contrast, focus, and target sizes

## Design loop for building or editing a screen

1. Identify the user's primary task on this screen.
2. Decide what the *one* primary action (if any) is.
3. Establish or confirm the system primitives (spacing scale, type styles, color roles, radii, shadows). If the project already has tokens, use them — don't invent new values.
4. Lay out content in this order: grouping → hierarchy → affordances. Get structure right before adding emphasis or interaction styling.
5. Run the audit checklist below; fix the biggest violations first.
6. Make the smallest change that increases consistency. Avoid random "magic tweaks" — every value should be traceable to the system.

## Core principles

### Coherence beats cleverness

Prefer predictable, repeated patterns over novelty. If an element breaks the pattern, it must be for a clear reason (e.g., the primary action). Novelty without reason reads as inconsistency, which humans experience as sloppiness.

### Grouping must be unambiguous

Humans infer "these belong together" via three perceptual cues:

- **proximity** — near things feel related
- **similarity** — things that look alike feel related
- **common region** — things sharing a container feel related

Make these cues *agree*. If spacing says A belongs to B, don't style A like it belongs to C. Conflicting grouping cues are the single biggest reason a layout feels "messy" even when everything is technically aligned.

### Hierarchy must be obvious at a glance

Use a small set of emphasis levers:

- **placement** — top/left in LTR contexts is naturally prominent
- **size and weight** — bigger and bolder reads as more important
- **contrast** — both color and value contrast carry weight
- **whitespace** — more space around an element makes it feel more important

If everything is emphasized, nothing is. Pick the one or two things that genuinely matter and let the rest recede.

### Rhythm is a quality signal

Create a spacing rhythm and stick to it.

- Use a spacing scale (tokens, CSS variables, Tailwind's scale) — never ad-hoc numbers.
- Use consistent padding inside similar components.
- Keep consistent gaps between similar relationships: label→field, card→card, section→section.

When spacing becomes arbitrary, people feel the inconsistency even if they can't name it. Rhythm is one of the strongest subconscious cues of polish.

### Readability is a design feature

- Constrain reading width for long-form text. Aim roughly for 50–75 characters per line for body copy; outside that range, scanning gets tiring.
- Use a stable typographic set — a few text styles (title, section heading, body, caption) is usually enough.
- Avoid walls of text. Add headings, short paragraphs, and lists when content is long.

### Accessibility is part of aesthetics

Accessibility constraints aren't just compliance; they directly drive whether a UI feels comfortable, especially under stress, glare, fatigue, or aging vision.

- **Text contrast**: at least 4.5:1 for normal text, 3:1 for large text.
- **Non-text contrast**: at least 3:1 for icons, control boundaries, and focus indicators against adjacent colors.
- **Don't rely on color alone** to convey meaning (errors, required fields, status, selection). Pair with text, icons, shape, or position.
- **Visible focus** — focus indicators must be clearly visible and never hidden by sticky headers, modals, or toasts.
- **Target size** — interactive targets at least 24×24 CSS pixels, with breathing room around them.
- **Reduced motion** — respect `prefers-reduced-motion`; keep motion functional rather than decorative.

## Implementation guardrails

### Layout and spacing

- Prefer left alignment for text-heavy layouts (in LTR locales).
- Use a max content width for reading-intensive containers.
- Use consistent gutters and align key edges (text baselines, card edges, form columns).
- Don't mix multiple grid ideas on one screen — random center alignment alongside random left alignment reads as chaos.
- Prefer fewer, clearer groups over many partial groups. When density gets high, defer rare or advanced actions to secondary UI (progressive disclosure) rather than cramming everything into the primary view.

### Typography

- Keep to a small number of text styles. Title / section heading / body / caption is often enough.
- Use consistent line-height within each text style.
- Use font weight sparingly. Reserve strong weight for true headings or primary emphasis.
- Use typography to signal *importance and grouping*, not decoration.

### Color

- Use semantic color roles (background, surface, text, primary, secondary, error, border) rather than scattering raw hex values. This turns color choice into a constrained mapping problem: "what role is this element playing?" rather than "what random blue looks nice here?"
- Keep saturation limited in large areas; reserve vivid color for small, meaningful accents.
- Verify contrast in *every* theme you support (light and dark) — a token-based approach makes this tractable.

### Components and states

- Interactive elements must look interactive. Buttons should look like buttons; links should look like links.
- Every interactive element needs clear states: default, hover (where relevant), active, disabled, focus, error.
- If you use elevation or shadows, use them consistently to represent layering — not as decoration.

### Motion

- Motion should explain: what changed, where did it go, what happened?
- Avoid decorative motion on frequent interactions. The system already provides subtle animations; piling more on top creates fatigue.
- Prefer simple fades and small position shifts over large zooms or parallax — those are more likely to trigger vestibular discomfort.
- Honor `prefers-reduced-motion`; the UI should remain understandable with motion reduced or disabled.

## Audit checklist

Run this after building or editing a screen. Fix the biggest violations first.

### Structure and grouping
- [ ] Can I point to clear visual chunks (sections, cards, groups) without ambiguity?
- [ ] Do spacing, containers, and typography all agree about what's grouped?

### Alignment and rhythm
- [ ] Do the main edges and columns align (cards, headings, form fields)?
- [ ] Are paddings and gaps drawn from a consistent spacing scale?

### Hierarchy
- [ ] Is the primary action visually primary — and is *only* one thing "most important"?
- [ ] Are headings visibly headings, not just slightly bigger body text?
- [ ] Is secondary information de-emphasized without becoming unreadable?

### Readability
- [ ] Body text isn't overly wide; scanning feels easy.
- [ ] Paragraphs are short enough to scan; headings and lists are used when helpful.

### Accessibility basics
- [ ] Text contrast meets thresholds; UI boundaries and focus indicators are visible.
- [ ] Focus isn't hidden behind sticky headers, modals, or toasts.
- [ ] Tap and click targets are large enough and not tightly packed.
- [ ] Meaning isn't conveyed by color alone (error, success, required, selection).

### Motion discipline
- [ ] Animations are functional, not decorative.
- [ ] The UI remains understandable with animation reduced or disabled.

## Common mistakes and fixes

| Problem | Fix |
|---|---|
| Too many font sizes/weights | Reduce to a small set of text styles; re-apply hierarchy with spacing and contrast instead |
| Random spacing values | Introduce a spacing scale; refactor margins, padding, and gaps to tokens |
| Border soup (everything outlined) | Use whitespace and grouping first; reserve borders for real separation or input delineation |
| Everything centered | Default to left-aligned text and a clear content column; center only when it aids comprehension |
| Weak affordances (links/buttons look like plain text) | Add consistent interactive styling and states (especially focus and disabled), and ensure targets are comfortably clickable |
| Color used as the only signal | Pair color with text, icon, shape, or position so meaning survives in grayscale |
| Decorative motion on frequent interactions | Strip it; reserve expressive motion for rare, meaningful moments |

## When to reach for the theory reference

Read `references/theory.md` when:

- You're justifying a design decision to the user and need the underlying research (Gestalt grouping, the aesthetic-usability effect, F-pattern scanning).
- An edge case isn't covered by the checklist and you need to reason from first principles.
- You're auditing an existing design and want to articulate *why* something feels off, not just that it does.
- You're working in an unusual medium (not a typical web/app UI) and need to translate the principles to a new context.
