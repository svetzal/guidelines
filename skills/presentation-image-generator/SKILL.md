---
name: presentation-image-generator
description: Generate images for Slidev presentations including covers (16:9), section breaks (16:9), concepts (1:1), backgrounds (16:9), and accents (1:1). Abstract-first approach — character is OFF by default. Supports multiple visual styles via scene variants. Use when creating presentation imagery, generating slide visuals, or adding custom graphics to a talk.
---

# Presentation Image Generator

This skill generates images for Slidev presentations using an abstract-first approach. Unlike the blog image generator (which centers on a recurring character), presentation images are primarily conceptual, atmospheric, and designed to integrate with Slidev's layout system.

## When to Use This Skill

- Creating images for a new or existing Slidev presentation
- User asks to generate cover art, section break visuals, or concept illustrations for slides
- User mentions "presentation image", "slide image", "cover image for talk", "slide background"
- Adding visual polish to a presentation deck

## Image Roles

| Role | Default Aspect | Default Size | Purpose |
|------|---------------|-------------|---------|
| `cover` | 16:9 | 1536x1024 | Title/hero slide, dramatic |
| `section-break` | 16:9 | 1536x1024 | Atmospheric transition between sections |
| `concept` | 1:1 | 1024x1024 | Visualizes an abstract idea |
| `comparison` | 16:9 | 1536x1024 | Before/after or contrast visual |
| `diagram` | 9:16 | 1024x1536 | Process or architecture diagram |
| `background` | 16:9 | 1536x1024 | Subtle texture behind text |
| `accent` | 1:1 | 1024x1024 | Small inline visual element |

Character is **OFF by default** for all roles. Use `--with-character` or include a `Character` block in the spec to enable.

## Scene Variants (Visual Styles)

Choose a scene variant to set the visual direction for the entire deck or individual images:

| Variant | File | Best For |
|---------|------|----------|
| **Clean Tech** | `scene-variants/clean-tech.json` | Professional conference talks |
| **Abstract Data** | `scene-variants/abstract-data.json` | Technical/analytical talks |
| **Cyberpunk** | `scene-variants/cyberpunk.json` | Edgy/provocative talks |
| **Organic** | `scene-variants/organic.json` | Sustainability, human-systems talks |
| **Architectural** | `scene-variants/architectural.json` | Process/methodology talks |

Each variant provides a complete `Style` block with Genre, Rendering, Lighting, ColorPalette, and Atmosphere.

## Character Variants (Optional)

For talks that include the presenter character (personal storytelling, keynotes):

| Variant | File | Purpose |
|---------|------|---------|
| **Presenter** | `character-variants/presenter.json` | Professional, approachable |
| **Cyberpunk** | `character-variants/cyberpunk.json` | Dramatic, edgy |

## Procedure for Creating Presentation Images

### Step 1: Choose the Scene Variant

Read the appropriate scene variant file from `scene-variants/`. Use a single variant across the entire deck for visual consistency, or mix variants intentionally for contrast.

### Step 2: Read the Baseline for the Image Role

Read the baseline file from `baselines/` that matches the image role:

- `baselines/cover.json` — Cover/hero images
- `baselines/section-break.json` — Section transition images
- `baselines/concept.json` — Abstract concept illustrations
- `baselines/background.json` — Subtle text backgrounds
- `baselines/accent.json` — Small inline visuals

Also read the schema at `baselines/presentation-scene.schema.json` for the full field reference.

### Step 3: Create the Scene JSON

Create a JSON file in the presentation's `public/images/` directory. Only `ImageRole` and `ContentDescription` are required — everything else is optional refinement.

**Minimal spec (just 2 fields):**

```json
{
  "ImageRole": "cover",
  "ContentDescription": "An expansive network of glowing nodes representing interconnected teams, floating in a dark space with warm amber connections pulsing between them"
}
```

**Full spec with all optional blocks:**

```json
{
  "ImageRole": "concept",
  "ContentDescription": "A single tangled knot of wires gradually untangling into clean, organized cables — representing the journey from complexity to clarity",

  "Layout": {
    "SlidevLayout": "image-right",
    "AspectRatio": "1:1",
    "TextSafeZone": "none",
    "FocalPoint": "center",
    "NegativeSpace": "moderate"
  },

  "PresentationContext": {
    "TalkTitle": "Untangling Legacy Systems",
    "SlideNumber": 12,
    "SectionName": "The Path Forward",
    "SlideTitle": "From Chaos to Clarity",
    "NarrativeRole": "resolution",
    "Mood": "optimistic",
    "Themes": ["refactoring", "incremental improvement", "patience"],
    "VisualContinuity": "Earlier slides showed progressively more tangled wires — this is the payoff"
  },

  "Style": {
    "Genre": "Modern Tech / Minimal Corporate",
    "Rendering": "Clean digital illustration, polished, editorial quality",
    "Lighting": {
      "Type": "Clean, warm, inviting",
      "Sources": ["Soft ambient light", "Warm glow from organized section"],
      "Shadows": "Soft, fading into clean space"
    },
    "ColorPalette": {
      "Primary": ["Steel Blue", "Pure White", "Light Grey"],
      "Accents": ["Warm Amber", "Soft Gold"],
      "Treatment": "Cool tones for the tangled section, warm tones for the organized section"
    },
    "Atmosphere": {
      "Effects": ["Subtle gradient", "Clean geometric background"],
      "Mood": "Hopeful transition from complexity to order"
    }
  },

  "Situation": {
    "Name": "The Untangling",
    "Setting": "Abstract space, gradient from dark (complex) to light (clear)",
    "Camera": "Straight-on, centered on the transition point",
    "Props": {
      "Conceptual": [
        {
          "Name": "Tangled wire cluster",
          "Description": "Dense knot of colorful wires, slightly chaotic",
          "Application": "Left side of frame",
          "SymbolicMeaning": "Legacy complexity"
        },
        {
          "Name": "Organized cable run",
          "Description": "Clean, labeled, color-coded cables emerging from the knot",
          "Application": "Right side of frame",
          "SymbolicMeaning": "Refactored clarity"
        }
      ]
    }
  },

  "PromptKeywords": [
    "clean design", "minimal", "conceptual illustration",
    "transformation", "order from chaos"
  ],

  "CompositionNotes": "The transition from tangled to organized should flow naturally left-to-right. The organized side should feel lighter, warmer, and more spacious."
}
```

### Step 4: Generate the Image

Run the generation script from the repository root:

```bash
# First time setup
cd .claude/skills/presentation-image-generator/scripts
npm install
cd ../../../..

# Generate (no character by default)
node .claude/skills/presentation-image-generator/scripts/generate-image.mjs \
  presentations/my-talk/public/images/cover.json \
  presentations/my-talk/public/images/cover.png

# Generate with character reference (for personal storytelling slides)
node .claude/skills/presentation-image-generator/scripts/generate-image.mjs \
  presentations/my-talk/public/images/speaker.json \
  presentations/my-talk/public/images/speaker.png \
  --with-character
```

Requires `OPENAI_API_KEY` environment variable.

**Default behavior:** All image roles generate without character reference (abstract mode). Character is enabled by:
1. Using `--with-character` flag
2. Including a `Character` block in the scene JSON

### Step 5: Reference in Slides

Place images in the presentation's `public/images/` directory and reference them in Slidev:

```markdown
---
layout: cover
background: /images/cover.png
---

# Talk Title
```

Or for image layouts:

```markdown
---
layout: image-right
image: /images/concept.png
---

# The Key Insight

Content alongside the image
```

Or inline with HTML:

```html
<img src="/images/accent.png" class="w-40 rounded shadow" />
```

## Layout Integration

The `Layout` block in the scene spec maps directly to Slidev's layout system:

| Layout.SlidevLayout | How Image Is Used | Key Consideration |
|---------------------|-------------------|-------------------|
| `cover` | Full-bleed background | Keep center clear for title text |
| `image` | Full-screen image | Can use entire frame |
| `image-right` | Right half of slide | Left side has text — keep focal point on image side |
| `image-left` | Left half of slide | Right side has text — keep focal point on image side |
| `section` | Background behind section title | Keep center clear, subtle |
| `default` | Inline via `<img>` tag | Will be displayed smaller, needs clear subject |

**TextSafeZone** tells the image generator which region to keep visually quiet:
- `center` — for cover/section layouts where title text is centered
- `left-third` — for image-right layouts where text is on the left
- `right-third` — for image-left layouts where text is on the right
- `none` — for standalone images (image layout, inline)

## File Organization

```
presentations/my-talk/
├── slides.md
└── public/
    └── images/
        ├── cover.json          # Cover image spec
        ├── cover.png           # Generated cover image
        ├── section-testing.json
        ├── section-testing.png
        ├── concept-tdd.json
        ├── concept-tdd.png
        └── bg-subtle.json
        └── bg-subtle.png
```

## Deck-Wide Visual Consistency

For a cohesive deck, follow these guidelines:

1. **Choose one scene variant** for the entire deck (e.g., `clean-tech` for a conference talk)
2. **Use consistent `VisualContinuity` notes** in `PresentationContext` to thread motifs across images
3. **Reserve accent colors** for emphasis — don't use them in every image
4. **Maintain a mood arc** — the deck's emotional progression should be reflected in the images (e.g., start contemplative, build to energetic, resolve to optimistic)

## Reference Files

| File | Purpose |
|------|---------|
| `baselines/presentation-scene.schema.json` | Full JSON Schema for scene specifications |
| `baselines/cover.json` | Baseline for cover images |
| `baselines/section-break.json` | Baseline for section break images |
| `baselines/concept.json` | Baseline for concept illustrations |
| `baselines/background.json` | Baseline for subtle backgrounds |
| `baselines/accent.json` | Baseline for small inline visuals |
| `scene-variants/*.json` | Visual style presets (5 variants) |
| `character-variants/*.json` | Character presets (2 variants, optional) |

## Differences from Blog Image Generator

| Aspect | Blog Images | Presentation Images |
|--------|------------|---------------------|
| Character | ON by default (banners) | OFF by default (all roles) |
| Required fields | ImageType, Character, Style, Situation, PromptKeywords | ImageRole, ContentDescription only |
| Primary approach | Character-driven scenes | Abstract/conceptual visuals |
| Layout awareness | None (standalone images) | Slidev layout integration |
| Scene variants | 4 (cyberpunk, winter-forest, boardroom, coffeeshop) | 5 (clean-tech, abstract-data, cyberpunk, organic, architectural) |
| Output location | `posts/YYYY/images/` | `presentations/<slug>/public/images/` |

## Troubleshooting

- **API errors**: Ensure `OPENAI_API_KEY` is set and valid
- **Missing dependencies**: Run `npm install` in the scripts directory
- **Character reference not found**: Ensure `assets/avatar.jpg`, `assets/stacey.jpg`, and `assets/stacey2.jpg` exist, or use `--no-character`
- **Wrong size**: Check `ImageRole` and `Layout.AspectRatio` — the aspect ratio override takes precedence
- **Image too busy for background**: Use the `background` role baseline — it has very low contrast defaults
- **Text unreadable over image**: Increase `NegativeSpace` to `generous` and set `TextSafeZone` appropriately
- **Images don't match across deck**: Use the same scene variant for all images and thread `VisualContinuity` notes
