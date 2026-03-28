# Slidev Diagrams and Math Reference

Mermaid diagrams, PlantUML, and KaTeX math rendering.

## Mermaid Diagrams

Supported natively. Use fenced code blocks with `mermaid` language:

````markdown
```mermaid
graph LR
  A[Start] --> B{Decision}
  B -->|Yes| C[Action]
  B -->|No| D[Other Action]
  C --> E[End]
  D --> E
```
````

### Common Diagram Types

**Flowchart:**

````markdown
```mermaid
graph TD
  A[Input] --> B[Process]
  B --> C[Output]
```
````

Direction: `TD` (top-down), `LR` (left-right), `BT` (bottom-top), `RL` (right-left).

**Sequence Diagram:**

````markdown
```mermaid
sequenceDiagram
  participant U as User
  participant S as Server
  participant D as Database
  U->>S: Request
  S->>D: Query
  D-->>S: Result
  S-->>U: Response
```
````

**Class Diagram:**

````markdown
```mermaid
classDiagram
  class Animal {
    +String name
    +move()
  }
  class Dog {
    +bark()
  }
  Animal <|-- Dog
```
````

**State Diagram:**

````markdown
```mermaid
stateDiagram-v2
  [*] --> Idle
  Idle --> Processing: Start
  Processing --> Done: Complete
  Processing --> Error: Fail
  Error --> Idle: Reset
  Done --> [*]
```
````

**Gantt Chart:**

````markdown
```mermaid
gantt
  title Sprint Plan
  section Backend
  API Design :a1, 2024-01-01, 3d
  Implementation :a2, after a1, 5d
  section Frontend
  UI Mockup :b1, 2024-01-01, 2d
  Components :b2, after b1, 4d
```
````

**Pie Chart:**

````markdown
```mermaid
pie title Test Coverage
  "Covered" : 73
  "Uncovered" : 27
```
````

### Mermaid Configuration

Set theme and scale via frontmatter directive within the code block:

````markdown
```mermaid {theme: 'neutral', scale: 0.8}
graph LR
  A --> B
```
````

Themes: `default`, `neutral`, `dark`, `forest`, `base`.

### Tips for Slides

- Keep diagrams under 8 nodes for readability
- Use `LR` (left-right) for process flows on wide slides
- Use `TD` (top-down) for hierarchies
- Abbreviate labels — full descriptions go in speaker notes
- Consider using v-click with multiple diagram versions for progressive reveal

## PlantUML

Requires the `@slidev/plugin-plantuml` addon. Less commonly used than Mermaid.

````markdown
```plantuml
@startuml
actor User
User -> Server: Request
Server -> Database: Query
Database --> Server: Result
Server --> User: Response
@enduml
```
````

## KaTeX Math

Renders LaTeX math expressions. Enabled by default.

### Inline Math

```markdown
The formula $E = mc^2$ is famous.

When $n$ approaches infinity, $\sum_{i=1}^{n} \frac{1}{i}$ diverges.
```

### Block Math

```markdown
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

### Common Patterns

**Fractions:**

```markdown
$$\frac{a}{b}$$
```

**Subscripts/Superscripts:**

```markdown
$$x_i^2 + y_i^2 = r^2$$
```

**Matrices:**

```markdown
$$
\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
$$
```

**Summations:**

```markdown
$$\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n$$
```

### Chemical Equations (mhchem)

Using the mhchem extension:

```markdown
$$\ce{H2O -> H2 + 1/2 O2}$$
$$\ce{CO2 + H2O -> H2CO3}$$
```

### Tips for Slides

- Use inline math `$...$` for formulas within text
- Use block math `$$...$$` for standalone equations
- Keep equations simple on slides — put derivations in speaker notes
- Large matrices are hard to read on slides; consider splitting across slides
