# Slidev Code Features Reference

Code highlighting, Magic Move, Monaco editor, and snippets.

## Line Highlighting

### Static Highlighting

Highlight specific lines with `{lines}` after the language:

````markdown
```ts {2,3}
const a = 1
const b = 2    // highlighted
const c = 3    // highlighted
const d = 4
```
````

**Syntax:**

- `{2}` — single line
- `{2,5}` — lines 2 and 5
- `{2-5}` — lines 2 through 5
- `{2,4-6,8}` — combine ranges
- `{*}` — highlight all lines
- `{0}` — highlight no lines (show all dimmed)

### Click-Stepped Highlighting

Different highlights on each click, separated by `|`:

````markdown
```ts {1|2-3|5}
const name = 'Slidev'     // click 1
const greeting = 'Hello'  // click 2
const msg = `${greeting}, ${name}`  // click 2
                           // gap
console.log(msg)           // click 3
```
````

The `{*|1|2-3}` pattern means: show all → highlight line 1 → highlight lines 2-3.

Use `{*|...|*}` to start and end with all lines visible:

````markdown
```ts {*|2|4|*}
line 1
line 2  // click 1: highlight
line 3
line 4  // click 2: highlight
```
````

### At Modifier

Control when highlighting starts relative to other clicks:

````markdown
```ts {1|2|3}{at:5}
first   // appears at click 5
second  // appears at click 6
third   // appears at click 7
```
````

## Line Numbers

### Global Setting

```yaml
# In headmatter
lineNumbers: true
```

### Per-Block

````markdown
```ts {1,2}{lines:true}
const a = 1
const b = 2
```
````

Start from a specific number:

````markdown
```ts {}{lines:true,startLine:5}
// This shows as line 5
// This shows as line 6
```
````

## Max Height

Scrollable code blocks:

````markdown
```ts {*}{maxHeight:'200px'}
// Long code here
// Will scroll within 200px
```
````

## Shiki Magic Move

Animated transitions between code states. Wrap multiple code blocks with 4 backticks:

`````markdown
````md magic-move
```js
const greeting = 'hello'
```
```js
const greeting = 'hello'
const audience = 'world'
```
```js
const greeting = 'hello'
const audience = 'world'
console.log(`${greeting}, ${audience}!`)
```
````
`````

Each code block is a step, transitioned on click. The animation morphs matching tokens.

### Magic Move with Highlighting

`````markdown
````md magic-move {lines:true}
```js {*|1|2}
const a = 1
```
```js
const a = 1
const b = 2
```
````
`````

### Magic Move with Title Bar

`````markdown
````md magic-move
```js [app.js]
console.log('Step 1')
```
```js [app.js]
console.log('Step 2')
```
````
`````

### Magic Move Options

| Option | Default | Description |
|--------|---------|-------------|
| `duration` | 800 | Animation duration in ms |

Global config in headmatter:

```yaml
magicMoveDuration: 500
magicMoveCopy: true       # true | false | 'final'
```

## Monaco Editor

Interactive code editor embedded in slides. Enable in headmatter:

```yaml
monaco: true
```

### Read-Only Editor

````markdown
```ts {monaco}
const greeting = 'hello world'
console.log(greeting)
```
````

### Editable Editor

````markdown
```ts {monaco}
// Audience can edit this live
function add(a: number, b: number) {
  return a + b
}
```
````

### Diff View

````markdown
```ts {monaco-diff}
const original = 'hello'
~~~
const modified = 'world'
```
````

The `~~~` separates the original (top) from the modified (bottom).

### Runnable Code

````markdown
```ts {monaco-run}
console.log('This runs in the browser!')
```
````

Adds a "Run" button. Output appears below the editor. Requires a code runner (built-in for JS/TS).

## Code Snippets (External Files)

Import code from external files:

````markdown
```ts
<<< @/snippets/example.ts
```
````

With line highlighting:

````markdown
```ts {2,3}
<<< @/snippets/example.ts
```
````

Import specific lines:

````markdown
```ts
<<< @/snippets/example.ts#region-name
```
````

The `@` resolves to the presentation root directory. Store snippets in a `snippets/` directory:

```
presentations/my-talk/
├── slides.md
└── snippets/
    ├── before.ts
    └── after.ts
```

## Code Groups

Tabbed code blocks for showing alternatives:

````markdown
:::code-group

```ts [TypeScript]
const greeting: string = 'hello'
```

```js [JavaScript]
const greeting = 'hello'
```

```py [Python]
greeting = 'hello'
```

:::
````

Each tab is labeled with the text in `[brackets]`.

## Copy Button

Controlled globally or per-block:

```yaml
# In headmatter
codeCopy: true    # true | false | 'hover'
```
