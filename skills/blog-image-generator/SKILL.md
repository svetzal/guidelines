---
name: blog-image-generator
description: Generate cyberpunk-styled images for blog posts including banners (16:9), callouts (1:1), and diagrams (9:16). Use this skill when creating new blog posts, when asked to generate images, or when updating visuals for existing posts. Creates consistent character-based imagery following the blog's visual identity.
---

# Blog Image Generator

This skill generates images for blog posts using a consistent cyberpunk visual style featuring a silver-haired woman systems thinker as the recurring character.

## When to Use This Skill

- Creating a new blog post that needs a banner image
- Adding inline illustrations (callouts) within an article
- Creating infographic-style diagrams to explain concepts
- User asks to generate, create, or update any blog image
- User mentions "generate image", "create banner", "add illustration", or "make diagram"

## Image Types

| Type | Aspect Ratio | Size | Purpose | Character Reference |
|------|--------------|------|---------|---------------------|
| `banner` | 16:9 | 1536x1024 | Hero image at top of article | Yes (default) |
| `callout` | 1:1 | 1024x1024 | Inline illustration emphasizing a specific point | No (optional) |
| `diagram` | 9:16 | 1024x1536 | Tall infographic explaining a process or system | No (default) |

## Character Consistency

The script uses multiple reference images to maintain character consistency across all generated images. This ensures the protagonist looks the same in every banner.

**Reference images** (in `assets/`):
- `avatar.jpg` — Original avatar image
- `stacey.jpg` — Primary character reference
- `stacey2.jpg` — Additional angle/pose reference

All three images are passed together to the OpenAI image edit API, giving the model multiple views of the character for better consistency.

**How it works:**
- For `banner` images: Uses all character references by default (via OpenAI's image edit API)
- For `callout` images: No character reference by default (use `--with-character` for character-focused callouts)
- For `diagram` images: No character reference by default (abstract/infographic style)

**Override flags:**
- `--with-character` — Force use of character references (e.g., for character-focused callouts)
- `--no-character` — Skip character references (e.g., for abstract banners without the character)

## The Visual System

All images share a consistent character and style:

### The Character

A middle-aged, silver-haired woman with blue-grey eyes — an experienced coder and systems thinker. She has a sturdy Eastern European build with broad shoulders. She typically wears a dark blazer over tech-casual attire, sleeves pushed up.

**Base wardrobe** (always present):
- Dark professional blazer bridging corporate and technical worlds

**Situational wardrobe** (context-dependent):
- Leather coat with high collar (outdoor/street scenes)
- Professional glasses with modern frames (close-up work)
- Futuristic sunglasses (outdoor urban, adds mystery)

### The Style

- **Genre**: Cyberpunk / Tech Noir
- **Rendering**: High-detail digital painting, photorealistic, concept art quality
- **Lighting**: Dramatic, high-contrast, cinematic (neon signs, screen glow, rim lighting)
- **Colors**: Magenta, Cyan, Electric Blue, Lime Green with Silver/White accents
- **Atmosphere**: Bokeh, atmospheric haze, neon glow, reflections

## Procedure for Creating Images

### Step 1: Analyze the Article

Read the article content and identify:

1. **Mood**: Is it optimistic, analytical, frustrated, or contemplative?
2. **Key themes**: What concepts need visual representation?
3. **Symbolic elements**: What objects or metaphors appear in the text?
4. **Image placement**: Banner (top), callout (inline), or diagram (process explanation)?
5. **Character presence**: Does this image need the character, or is it prop/concept focused?

### Step 2: Choose Props

Props are categorized by their source:

**Character Props** — Items belonging to the character:
- Wardrobe items from the base design (blazer, glasses, etc.)
- Personal items (coffee mug, mechanical keyboard)
- These provide consistency across images

**Article Props** — Objects derived from article content:
- Symbolic representations of concepts (tangled cables = complexity)
- Specific items mentioned in the text (red stapler from Office Space)
- Visual metaphors (approval gates, holographic whiteboards)
- These make each image unique to its article

**Environment Props** — Part of the setting:
- Furniture, architecture, background elements
- These establish context and mood

### Step 3: Design the Situation

Create a scene that visually complements the article:

**For optimistic articles:**
- Warmer lighting with amber and gold accents
- Collaborative scenes, open spaces
- Character expression: slight smile, engaged, forward-leaning

**For analytical articles:**
- Cool blue-dominant lighting, screen glow emphasis
- Clean, organized environment
- Character expression: focused concentration, slight squint

**For frustrated articles:**
- Harsh contrasts, red/amber warning tones
- Cluttered or chaotic elements
- Character expression: tension in jaw, exasperated gaze

**For contemplative articles:**
- Soft, diffused single-source lighting
- Quiet, still environment
- Character expression: distant gaze, thoughtful half-smile

### Step 4: Create the Scene JSON

Create a JSON file in `posts/YYYY/images/` with the same base name as the target image.

Example: For an article at `posts/2025/2025-12-29-my-article.md`:
- Banner image: `posts/2025/images/my-banner.json` → `my-banner.png`
- Callout image: `posts/2025/images/my-callout-1.json` → `my-callout-1.png`

**Scene JSON Structure:**

```json
{
  "ImageType": "banner",

  "Character": {
    "Description": "A highly competent, focused woman coder and systems thinker",
    "Age": "Middle-aged, mature, experienced",
    "Ethnicity": "Eastern European build",
    "Build": {
      "Type": "Heavy set, sturdy",
      "UpperBody": "Big arms, broad shoulders",
      "LowerBody": "Slim hips"
    },
    "Face": {
      "Eyes": "Blue-grey",
      "Expression": "Thoughtful, analytical"
    },
    "Hair": {
      "Color": "Grey/silver",
      "Length": "Long",
      "Style": "Wind-swept or naturally flowing"
    },
    "Wardrobe": {
      "Base": [
        {
          "Name": "Dark blazer",
          "Description": "Professional dark blazer over tech-casual attire, sleeves pushed up",
          "Context": "Always present"
        }
      ]
    }
  },

  "Style": {
    "Genre": "Cyberpunk / Tech Noir",
    "Rendering": "High-detail digital painting, photorealistic, concept art quality",
    "Lighting": {
      "Type": "Dramatic, high-contrast, cinematic",
      "Sources": ["Neon signs", "Screen glow", "Rim lighting"],
      "Shadows": "Sharp, emphasizing texture and form"
    },
    "ColorPalette": {
      "Primary": ["Magenta", "Cyan", "Electric Blue", "Lime Green"],
      "Accents": ["Silver", "White", "Cool Blues", "Metallic purples"],
      "Treatment": "High saturation, strong contrast"
    },
    "Atmosphere": {
      "Effects": ["Bokeh", "Atmospheric haze", "Neon glow"],
      "Mood": "Mysterious, electric, high-stakes"
    }
  },

  "Situation": {
    "Name": "Descriptive Scene Name",
    "Setting": "Environment description matching article theme",
    "Camera": "Shot type and framing",
    "CharacterPose": {
      "Expression": "Specific facial expression for this scene",
      "BodyPosition": "How she's positioned",
      "Gesture": "What she's doing with hands/arms"
    },
    "Props": {
      "Character": [
        {
          "Name": "Professional glasses",
          "Description": "Modern rectangular frames",
          "Application": "Worn, screen reflections visible"
        }
      ],
      "Article": [
        {
          "Name": "Red stapler",
          "Description": "Iconic Swingline stapler with subtle red glow",
          "Application": "Sitting forgotten on desk",
          "SymbolicMeaning": "Overlooked humanity in systems"
        }
      ],
      "Environment": [
        {
          "Name": "Holographic whiteboard",
          "Description": "Translucent display with diagrams",
          "Application": "Floating beside subject"
        }
      ]
    },
    "KeyDetails": [
      "Visual element that tells the story",
      "Another atmospheric detail"
    ],
    "LightingFocus": "How lighting reinforces the mood",
    "ThematicTags": ["systems-thinking", "leadership"]
  },

  "ArticleContext": {
    "Title": "Article title",
    "Tags": ["tag1", "tag2"],
    "Themes": ["key concept 1", "key concept 2"],
    "Mood": "optimistic"
  },

  "PromptKeywords": [
    "highly detailed", "digital painting", "concept art",
    "cyberpunk", "neon light", "cinematic lighting", "high contrast"
  ]
}
```

### Step 5: Generate the Image

Run the generation script from the repository root:

```bash
# First time setup
cd .claude/skills/blog-image-generator/scripts
npm install
cd ../../../..

# Generate banner (uses character reference by default)
node .claude/skills/blog-image-generator/scripts/generate-image.mjs \
  posts/YYYY/images/scene-name.json \
  posts/YYYY/images/scene-name.png

# Generate callout with character (override default)
node .claude/skills/blog-image-generator/scripts/generate-image.mjs \
  posts/YYYY/images/callout.json \
  posts/YYYY/images/callout.png \
  --with-character

# Generate diagram or prop-focused callout (no character)
node .claude/skills/blog-image-generator/scripts/generate-image.mjs \
  posts/YYYY/images/diagram.json \
  posts/YYYY/images/diagram.png \
  --no-character
```

Requires `OPENAI_API_KEY` environment variable.

**Default behavior by image type:**
| Image Type | Default Mode | API Used |
|------------|--------------|----------|
| `banner` | With character | Image Edit API |
| `callout` | No character | Image Generate API |
| `diagram` | No character | Image Generate API |

### Step 6: Update Article Frontmatter

For banner images, update the article frontmatter:

```yaml
---
image: images/scene-name.png
imageAlt: "Description of the scene for accessibility"
---
```

The `imageAlt` should describe the scene in plain language for screen readers.

## Reference Files

The skill includes baseline specifications in `baselines/`:

- `scene.schema.json` — JSON Schema for scene specifications
- `banner.json` — Baseline for banner images (16:9)
- `callout.json` — Baseline for callout images (1:1)
- `diagram.json` — Baseline for diagram images (9:16)

The character reference images are in `assets/` in the repository root: `avatar.jpg`, `stacey.jpg`, and `stacey2.jpg`.

Copy the Character, Style, and PromptKeywords from the appropriate baseline when creating new scenes.

## Examples

### Example 1: Optimistic Problem-Solving Banner

Article about finding solutions despite obstacles. Uses character reference (default for banner).

```json
{
  "ImageType": "banner",
  "Situation": {
    "Name": "The Collaborative Breakthrough",
    "Setting": "Modern workspace with holographic whiteboard, warm lighting mixed with tech glow",
    "Camera": "Mid-shot, slightly wide, subject off-center with whiteboard visible",
    "CharacterPose": {
      "Expression": "Animated enthusiasm, eyebrows raised in discovery, slight smile",
      "BodyPosition": "Standing at whiteboard, weight forward on balls of feet",
      "Gesture": "One hand holding marker, other open-palmed inviting gesture"
    },
    "Props": {
      "Character": [
        {"Name": "Dark blazer", "Description": "Sleeves pushed up, ready for work", "Application": "Worn"}
      ],
      "Article": [
        {"Name": "Solution sketch", "Description": "Simple clean diagram on whiteboard", "Application": "Being drawn", "SymbolicMeaning": "Clarity from complexity"},
        {"Name": "Crossed-out flowchart", "Description": "Complex tangled diagram with X through it", "Application": "Visible on whiteboard", "SymbolicMeaning": "Rejected overcomplicated approach"}
      ],
      "Environment": [
        {"Name": "Collaborative seating", "Description": "Chairs with engaged colleague silhouettes", "Application": "Background"}
      ]
    },
    "LightingFocus": "Warm whiteboard glow on face, overall warmer tone for optimism"
  },
  "ArticleContext": {
    "Mood": "optimistic",
    "Themes": ["problem-solving", "collaboration", "clarity"]
  }
}
```

**Generate with:** `node generate-image.mjs banner.json banner.png` (character reference used by default)

### Example 2: Frustrated Bureaucracy Banner

Article about process overhead and organizational dysfunction.

```json
{
  "ImageType": "banner",
  "Situation": {
    "Name": "Navigating the Gate Maze",
    "Setting": "Surreal corporate corridor of translucent holographic approval gates",
    "Camera": "Mid-shot, wide angle, subject at junction where gate-paths converge",
    "CharacterPose": {
      "Expression": "Frustrated exhale, eyes rolled upward, jaw set with impatience",
      "BodyPosition": "Leaning on waist-high gate barrier, shoulders hunched",
      "Gesture": "Fingers drumming on gate surface"
    },
    "Props": {
      "Character": [
        {"Name": "Dark blazer", "Description": "Slightly rumpled from long day", "Application": "Worn"}
      ],
      "Article": [
        {"Name": "TPS report", "Description": "Floating document with cover sheet", "Application": "Drifting past", "SymbolicMeaning": "Pointless process"},
        {"Name": "Approval stamps", "Description": "APPROVED, PENDING, CAB REQUIRED stamps on gates", "Application": "Displayed on gate surfaces", "SymbolicMeaning": "Bureaucratic obstacles"}
      ],
      "Environment": [
        {"Name": "Holographic gates", "Description": "Semi-transparent barriers numbered 1-14", "Application": "Arranged in maze pattern"},
        {"Name": "Queue of workers", "Description": "Distant silhouettes waiting at checkpoints", "Application": "Background"}
      ]
    },
    "LightingFocus": "Cool blue gate-glow, amber 'pending' indicators, tension lighting"
  },
  "ArticleContext": {
    "Mood": "frustrated",
    "Themes": ["bureaucracy", "process-overhead", "organizational-dysfunction"]
  }
}
```

**Generate with:** `node generate-image.mjs banner.json banner.png`

### Example 3: Character-Focused Callout

Inline illustration featuring the character examining code. Use `--with-character` flag.

```json
{
  "ImageType": "callout",
  "Situation": {
    "Name": "Examining the Code",
    "Setting": "Dark workspace, screens as primary light source",
    "Camera": "Close-up, shallow depth of field, focused on face and screen",
    "CharacterPose": {
      "Expression": "Focused concentration, slight analytical squint",
      "BodyPosition": "Leaning toward screen",
      "Gesture": "One finger pointing at specific line of code"
    },
    "Props": {
      "Character": [
        {"Name": "Professional glasses", "Description": "Code reflected in lenses", "Application": "Worn"}
      ],
      "Article": [
        {"Name": "Code display", "Description": "Clean syntax-highlighted code on screen", "Application": "Primary light source", "SymbolicMeaning": "The detail that matters"}
      ]
    },
    "LightingFocus": "Screen glow as sole light source, intimate technical moment"
  }
}
```

**Generate with:** `node generate-image.mjs callout.json callout.png --with-character`

### Example 4: Prop-Focused Callout

Inline illustration of an object or concept without the character. Default for callout type.

```json
{
  "ImageType": "callout",
  "Situation": {
    "Name": "The Red Stapler",
    "Setting": "Abandoned cubicle desk, dim fluorescent lighting",
    "Camera": "Close-up, shallow depth of field, object-focused",
    "CharacterPose": {
      "Expression": "N/A - no character in frame",
      "BodyPosition": "N/A",
      "Gesture": "N/A"
    },
    "Props": {
      "Article": [
        {"Name": "Red Swingline stapler", "Description": "Iconic red stapler with subtle glow, worn and battered", "Application": "Center of frame, slight spotlight", "SymbolicMeaning": "Overlooked humanity, small dignities"}
      ],
      "Environment": [
        {"Name": "Dusty desk surface", "Description": "Forgotten papers, empty coffee ring stains", "Application": "Background texture"},
        {"Name": "Basement window", "Description": "Small window with dim light filtering through", "Application": "Background, suggests Milton's relocation"}
      ]
    },
    "LightingFocus": "Single spotlight on stapler, everything else in shadow"
  }
}
```

**Generate with:** `node generate-image.mjs callout.json callout.png` (no character by default)

## File Organization

After generation, each image should have a paired JSON file:

```
posts/2025/images/
├── article-banner.png        # Generated banner
├── article-banner.json       # Banner specification
├── article-callout-1.png     # First inline callout
├── article-callout-1.json    # Callout specification
├── article-diagram.png       # Process diagram
└── article-diagram.json      # Diagram specification
```

## Troubleshooting

- **API errors**: Ensure `OPENAI_API_KEY` is set and valid
- **Missing dependencies**: Run `npm install` in the scripts directory
- **Character reference not found**: Ensure `assets/avatar.jpg`, `assets/stacey.jpg`, and `assets/stacey2.jpg` exist, or use `--no-character`
- **Wrong character appearance**: Verify the avatar reference is being used (check for "Using character reference" in output)
- **Mood mismatch**: Check LightingFocus and CharacterPose.Expression fields
- **Props not appearing**: Ensure Application field describes clear placement
- **Inconsistent character**: Use `--with-character` flag to force avatar reference
