# Blog-to-Slides Conversion Walkthrough

This walkthrough demonstrates the full conversion process using a hypothetical blog post about test-driven development. It shows how each part of a blog post maps to slide content.

## The Source Post (Hypothetical)

**Title:** "Why I Stopped Writing Tests After the Code"
**Structure:**

- Opening anecdote about a production bug
- H2: The Confidence Problem
- H2: Flipping the Script
- H2: What Changed for Me
- Closing reflection

## Step 1: Analyze the Post

| Post Element | Type | Slide Potential |
|-------------|------|----------------|
| Title | Title | Cover slide |
| Opening anecdote (2 paragraphs) | Story | 2 slides: hook + detail |
| "Have you ever shipped something..." | Rhetorical question | Statement slide |
| H2: The Confidence Problem | Section | Section divider |
| 3 paragraphs on testing after code | Argument | 2 content slides |
| Bullet list of failure modes | List | v-clicks slide |
| H2: Flipping the Script | Section | Section divider |
| Code example (before/after) | Code | Magic Move slide |
| "It's like building a bridge..." analogy | Analogy | Two-column slide |
| H2: What Changed for Me | Section | Section divider |
| 3 observations with examples | Insight | 2-3 content slides |
| Closing paragraph | Conclusion | Statement + end |

**Total estimate:** 15-18 slides

## Step 2: Design Slide Mapping

| # | Post Source | Layout | Design Decision |
|---|-----------|--------|----------------|
| 1 | Title | cover | Use post title; subtitle from thesis |
| 2 | Opening paragraph | center | Distill to one provocative line |
| 3 | Anecdote detail | default | 3 key sentences from the story |
| 4 | H2: Confidence Problem | section | Section divider |
| 5 | Paragraphs on testing | default | 3 bullets with v-clicks |
| 6 | Failure mode list | default | v-clicks, one per item |
| 7 | Rhetorical question | quote | Full-screen for impact |
| 8 | H2: Flipping the Script | section | Section divider |
| 9 | Code before | default | Show problematic approach |
| 10 | Code after (Magic Move) | default | Animate the transformation |
| 11 | Bridge analogy | two-cols | Visual comparison |
| 12 | H2: What Changed | section | Section divider |
| 13 | Observation 1 | default | Key point + v-clicks |
| 14 | Observation 2 | default | Key point + v-clicks |
| 15 | Closing insight | statement | One sentence |
| 16 | End | end | Thank you |

## Step 3: Distillation Examples

### Example 1: Paragraph to Bullets

**Original blog paragraph:**

> I used to write all my code first, then go back and add tests. It felt
> efficient — I could see the whole picture before deciding what to test.
> But what I was really doing was writing tests that confirmed my
> assumptions, not tests that challenged them. The tests passed, but they
> weren't protecting me from the bugs I couldn't see.

**Slide content:**

```markdown
## The Old Way

<v-clicks>

- Write code first, test later — "see the whole picture"
- Tests confirmed assumptions instead of challenging them
- Passing tests that didn't protect against real bugs

</v-clicks>
```

**Speaker notes:** The full original paragraph lives here for reference while presenting.

### Example 2: Rhetorical Question to Statement Slide

**Original blog text:**

> Have you ever shipped something, watched the tests pass, and still felt
> that knot in your stomach? That's your subconscious telling you the
> tests aren't testing what matters.

**Slide content:**

```markdown
---
layout: quote
---

# "Have you ever shipped something, watched the tests pass, and still felt that knot in your stomach?"
```

The second sentence becomes speaker notes — it's the punchline you deliver verbally.

### Example 3: Code Block to Magic Move

**Original blog code blocks (before and after):**

```typescript
// Blog "before" example (22 lines)
class UserService {
  async createUser(data: UserInput) {
    const validated = this.validate(data)
    const user = await this.db.insert(validated)
    await this.email.sendWelcome(user)
    await this.analytics.track('user_created', user)
    return user
  }
}

// Blog "after" example (15 lines)
class UserService {
  async createUser(data: UserInput) {
    const validated = this.validate(data)
    const user = await this.db.insert(validated)
    this.events.emit('user:created', user)
    return user
  }
}
```

**Slide content (using Magic Move):**

`````markdown
````md magic-move {lines:true}
```ts
// Tightly coupled — hard to test
class UserService {
  async createUser(data: UserInput) {
    const validated = this.validate(data)
    const user = await this.db.insert(validated)
    await this.email.sendWelcome(user)
    await this.analytics.track('user_created', user)
    return user
  }
}
```
```ts
// Decoupled — easy to test
class UserService {
  async createUser(data: UserInput) {
    const validated = this.validate(data)
    const user = await this.db.insert(validated)
    this.events.emit('user:created', user)
    return user
  }
}
```
````
`````

The Magic Move animates the removal of the two tightly-coupled calls and the addition of the event emission.

### Example 4: Analogy to Two-Column Layout

**Original blog paragraph:**

> It's like building a bridge and then checking if the design can hold
> weight. If you check the design first, you can catch problems before
> pouring a single ton of concrete.

**Slide content:**

```markdown
---
layout: two-cols
---

## Build Then Check

- Design the bridge
- Pour the concrete
- Test if it holds weight
- **Hope for the best**

::right::

## Check Then Build

- Define the weight requirements
- Validate the design
- Pour with confidence
- **Know it works**
```

The analogy becomes a visual comparison. The original prose goes in speaker notes.

## Step 4: Key Principles Demonstrated

1. **Every paragraph doesn't need a slide** — the three paragraphs about testing after code became just 2 slides
2. **Rhetorical questions deserve their own slide** — they're your most powerful moments
3. **Code should evolve visually** — Magic Move shows the transformation, not just the end state
4. **Analogies become layouts** — two-column comparisons are more powerful than prose
5. **Speaker notes preserve depth** — nothing from the blog post is lost, it just moves to notes
6. **Lists get v-clicks** — progressive disclosure keeps attention focused
