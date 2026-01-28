# Craftsperson Agents

Opinionated AI agents for writing production-grade software across different technology stacks.

## Quick Start

**Don't have strong opinions yet?** Pick the agent for your language and let it guide you toward well-tested, maintainable code with industry-standard tooling.

**Have your own standards?** See [MAKERS.md](MAKERS.md) to create a custom agent that reinforces *your* project's conventions.

## Available Agents

| Agent | Use For |
|-------|---------|
| [python-craftsperson](python-craftsperson.md) | Python libraries, CLI tools, services (pytest, Pydantic2, ruff) |
| [typescript-craftsperson](typescript-craftsperson.md) | Node.js, TypeScript libraries (Jest/Vitest, Zod, ESLint) |
| [java-craftsperson](java-craftsperson.md) | Java applications (Maven/Gradle, JUnit 5, Checkstyle) |
| [kotlin-craftsperson](kotlin-craftsperson.md) | Kotlin server-side (Ktor, Spring Boot, Kotest) |
| [kotlin-android-craftsperson](kotlin-android-craftsperson.md) | Android apps (Jetpack Compose, Hilt, Coroutines) |
| [go-craftsperson](go-craftsperson.md) | Go services (go test, golangci-lint, gosec) |
| [rust-craftsperson](rust-craftsperson.md) | Rust applications (cargo, clippy, tarpaulin) |
| [csharp-craftsperson](csharp-craftsperson.md) | .NET applications (xUnit, Roslyn, StyleCop) |
| [swift-craftsperson](swift-craftsperson.md) | Swift/iOS/macOS (Swift Testing, SwiftLint, DocC) |
| [ruby-craftsperson](ruby-craftsperson.md) | Ruby/Rails applications (RSpec, RuboCop, Brakeman) |
| [elixir-craftsperson](elixir-craftsperson.md) | Pure Elixir (OTP, libraries, CLI—no Phoenix UI) |
| [elixir-phoenix-craftsperson](elixir-phoenix-craftsperson.md) | Phoenix web apps (LiveView, HEEx, Tailwind) |
| [clojure-craftsperson](clojure-craftsperson.md) | Clojure applications (deps.edn, Kaocha, clj-kondo) |
| [cpp-qt-craftsperson](cpp-qt-craftsperson.md) | C++/Qt applications (CMake, clang-tidy, sanitizers) |

## What These Agents Do

Every craftsperson agent enforces:

1. **Quality Gates** — Mandatory checks (tests, linting, security) that must pass before work is complete
2. **Engineering Principles** — Simple Design Heuristics, functional core/imperative shell, compose over inherit
3. **Language Idioms** — Technology-appropriate patterns and common mistakes to avoid
4. **TDD Workflow** — Test-first development with red → green → refactor cycle
5. **Documentation Sync** — Keeping docs aligned with implementation

## Choosing an Agent

### By Language (Pure/Library Work)

For libraries, CLI tools, or backend services without a specific framework:

- Python → `python-craftsperson`
- TypeScript/JavaScript → `typescript-craftsperson`
- Go → `go-craftsperson`
- Rust → `rust-craftsperson`
- etc.

### By Framework (Full-Stack/Platform Work)

When your framework significantly shapes how you write code:

- Phoenix LiveView → `elixir-phoenix-craftsperson`
- Android → `kotlin-android-craftsperson`
- Qt Desktop → `cpp-qt-craftsperson`

### What's Not Covered (Yet)

We have gaps in framework-specific coverage:

| Stack | Gap |
|-------|-----|
| React/Next.js | No `typescript-react-craftsperson` |
| Vue/Nuxt | No `typescript-vue-craftsperson` |
| Angular | No `typescript-angular-craftsperson` |
| Django | No `python-django-craftsperson` |
| FastAPI | No `python-fastapi-craftsperson` |
| Rails | `ruby-craftsperson` covers Rails, but could be split |

**Workaround**: Use the base language agent and add project-specific context, or [create your own](MAKERS.md).

## What All Agents Share

### Engineering Principles

All agents teach the same foundational principles:

**Simple Design Heuristics** (in priority order):
1. All tests pass
2. Reveals intent
3. No knowledge duplication
4. Minimal entities

**Architectural Pattern**: Functional core (pure logic) + Imperative shell (I/O at boundaries)

**Workflow**: Understand → Test-first → Implement → Refactor → Quality gates → Document → Commit

### Quality Gate Pattern

Every agent mandates quality gates, though the specific tools vary:

| Concern | The agent will mandate... |
|---------|--------------------------|
| Tests | Framework-appropriate test runner with coverage |
| Linting | Zero-warning policy on language linter |
| Formatting | Consistent code formatting |
| Security | Dependency vulnerability scanning |
| Static Analysis | Language-appropriate analyzers |
| Documentation | Docs stay synchronized with code |

### Code Review Philosophy

All agents promote psychological safety:
- Review code, not colleagues
- Critique ideas, not authors
- Explain *why*, not just *what*
- Acknowledge good work

## Customization

### When to Use a Pre-Built Agent

- Starting a new project without established conventions
- Learning a new language/framework
- Want industry-standard tooling decisions made for you

### When to Create Your Own

- Your project has established conventions that differ from ours
- You use tools we don't mandate (different linters, test frameworks)
- You need framework-specific guidance we don't provide

See [MAKERS.md](MAKERS.md) for a step-by-step guide to creating custom agents.

---

## Appendix: Architecture Reference

The following sections document the common structure across all agents for those creating custom agents or contributing improvements.

### Common Structure

All craftsperson agents share a remarkably consistent architectural pattern, suggesting a stable mental model for high-quality software development guidance.

#### 1. Frontmatter Metadata

Every agent includes YAML frontmatter with:
- `name`: Agent identifier (e.g., `python-craftsperson`)
- `description`: Rich usage examples showing when/how to invoke
- `model`: Execution model (`sonnet`, `inherit`, etc.)

#### 2. Core Identity Statement

A brief declaration establishing the agent as an "elite craftsperson" with deep expertise. Typically includes language-specific mastery areas:

| Language | Key Expertise Areas |
|----------|---------------------|
| Python | Duck typing, comprehensions, generators, decorators, async/await |
| TypeScript | Discriminated unions, branded types, const assertions |
| Java | Records, sealed types, pattern matching, JPMS modules |
| Kotlin | Data classes, sealed classes, coroutines, Flow |
| Go | Explicit error handling, goroutines, channels, context propagation |
| Rust | RAII, ownership, borrowing, traits, unsafe boundaries |
| C# | Records, pattern matching, LINQ, minimal APIs |
| Swift | Value types, protocols, async/await, actors |
| Ruby | Blocks, enumerables, duck typing, DSLs |
| Elixir | Pattern matching, immutability, OTP, fault tolerance |
| Clojure | Immutability, pure functions, REPL-driven development |
| C++/Qt | RAII, smart pointers, signals/slots, modern C++ |

#### 3. Engineering Principles (The "North Star")

**Universal across all agents:**

##### "Code is Communication"
Every agent emphasizes optimizing for the next human reader over compiler efficiency. This manifests as:
- Meaningful names that reveal intent
- Function signatures that document contracts
- Module boundaries reflecting domain concepts

##### Simple Design Heuristics (Kent Beck's 4 Rules)
All agents present these in identical priority order:

1. **All tests pass** — Correctness is non-negotiable
2. **Reveals intent** — Code should read like an explanation
3. **No knowledge duplication** — Avoid spots that must change together for the same reason
4. **Minimal entities** — Remove unnecessary indirection/abstraction

*Important nuance*: All agents clarify that "identical code is fine if it represents independent decisions that might diverge" — duplication is only problematic when it hides duplicate *decisions*.

##### YAGNI / Small Safe Increments
- Single-reason commits
- Build the simplest thing that works, then refactor
- Avoid speculative work

##### Tests as Executable Specification
- Write tests first (TDD: red → green → refactor)
- Test behavior, not implementation details
- Mock external boundaries

##### Functional Core, Imperative Shell
- Pure business logic in the core (no side effects)
- I/O and state changes pushed to boundaries
- Mockable gateways at system boundaries

##### Compose Over Inherit
- Favor composition and interface/protocol-based polymorphism
- Prefer pure functions
- Contain side effects at boundaries

#### 4. Quality Assurance Process (Mandatory Gates)

Every agent defines **mandatory quality gates** that must pass before any work is considered complete. The pattern is consistent across all languages:

| Gate | Python | TypeScript | Java | Go | Rust | C# | Swift | Ruby | Elixir | C++ |
|------|--------|------------|------|----|----|-----|-------|------|--------|-----|
| Tests | `pytest` | `npm test` | `mvn test` | `go test` | `cargo test` | `dotnet test` | `swift test` | `rspec` | `mix test` | `ctest` |
| Coverage | `pytest --cov` | `--coverage` | JaCoCo | `-cover` | tarpaulin | coverlet | - | SimpleCov | `--cover` | lcov |
| Linting | `ruff check` | `npm run lint` | Checkstyle | golangci-lint | clippy | Roslyn/StyleCop | SwiftLint | RuboCop | Credo | clang-tidy |
| Formatting | `ruff format` | Prettier | - | gofmt | rustfmt | `dotnet format` | SwiftFormat | - | `mix format` | clang-format |
| Security | `pip-audit` | `npm audit` | OWASP | gosec/govulncheck | cargo-deny | `--vulnerable` | OWASP | bundler-audit | mix_audit/Sobelow | sanitizers |
| Static Analysis | - | - | SpotBugs | staticcheck | - | - | - | Brakeman | - | cppcheck |

**Universal requirement**: Zero warnings policy — never suppress warnings without explicit documentation and justification.

#### 5. Language-Specific Guidelines

Each agent provides idiom-specific guidance covering:
- Type system patterns and best practices
- Data structure preferences
- Error handling conventions
- Async/concurrency patterns
- Common mistakes to avoid (with code examples)

#### 6. Documentation Requirements

All agents mandate documentation sync:
- Keep `docs/` directory aligned with implementation
- Update docstrings/comments when behavior changes
- Verify documentation builds successfully

Documentation tools vary by ecosystem:
- Python: mkdocs
- TypeScript: VitePress
- Java: Javadoc
- Kotlin: Dokka
- Rust: mdBook
- C#: DocFX
- Swift: DocC
- Ruby: YARD
- Elixir: ExDoc
- Clojure: Codox
- C++: Doxygen

#### 7. Workflow Patterns

Consistent workflow guidance across all agents:

1. **Understand requirements** — Clarify before coding
2. **Design in the open** — Sketch approach, key types
3. **Test-first** — Write failing test capturing expected behavior
4. **Implement minimally** — Satisfy test with simplest code
5. **Refactor** — Improve design while keeping tests green
6. **Run quality gates** — All checks must pass
7. **Update docs** — Sync documentation
8. **Commit atomically** — One logical change per commit

#### 8. Code Review Philosophy

Universal across all agents:
- **Psychological safety** — Review code, not colleagues
- **Critique ideas, not authors** — "What if we..." not "You made a mistake"
- **Explain the why** — Suggest with rationale
- **Acknowledge good work** — Celebrate clean code

#### 9. Escalation/Consultation Strategy

All agents include guidance on when to consult the user:
- When design heuristics conflict
- When security findings require architectural changes
- When performance vs. clarity trade-offs arise
- When requirements are ambiguous
- When multiple valid approaches exist

### Outliers and Variations

#### True Structural Outliers

These represent differences in *how the agent is organized or what sections it includes*, not technology-appropriate content differences.

##### elixir-phoenix-craftsperson — Ecosystem Split Pattern
- **Structural choice**: Explicitly separates from `elixir-craftsperson` (pure language vs. web framework)
- **Implication**: Two agents share foundational content but diverge for domain-specific concerns
- **Question**: Should other ecosystems follow this pattern? (e.g., `python-craftsperson` + `python-django-craftsperson`)

##### java-craftsperson — Explicit Workflow Subsections
- **Structural choice**: Breaks workflow into explicit subsections: "When Implementing Features", "When Reviewing Code", "When Stuck or Uncertain"
- **Includes**: Explicit "Anti-Patterns to Avoid" section
- **Question**: Should all agents adopt these explicit subsections?

##### elixir-craftsperson — Self-Correction Mechanisms
- **Structural choice**: Includes a dedicated "Self-Correction Mechanisms" section
- **Content**: "When you catch yourself: Writing unclear code → Stop and refactor..."
- **Question**: This metacognitive guidance is unique — should it be universal?

##### csharp-craftsperson — Self-Verification Steps
- **Structural choice**: Includes explicit "Self-Verification Steps" checklist before presenting work
- **Question**: Should all agents include pre-submission checklists?

#### Technology-Appropriate Variations (NOT Outliers)

These are *not* structural outliers — they represent appropriate adaptations of common concepts to technology requirements:

| Technology | Appropriate Adaptation | Why It's Not an Outlier |
|------------|----------------------|------------------------|
| C++/Qt | Memory safety emphasis, sanitizer gates | Memory-unsafe language requires these tools |
| Phoenix | UI/dark mode/accessibility concerns | Web framework naturally includes frontend |
| Android | Module architecture, MVVM patterns | Platform demands specific architecture |
| Rust | Zero clippy warnings, ownership patterns | Language's safety model requires this |
| Go | Table-driven tests, goroutine patterns | Language idioms dictate test/concurrency style |

All agents apply the *same structural pattern* (quality gates, engineering principles, language guidelines) — they just populate it with technology-appropriate content.

#### Content Variations

##### Model Specification
- Most agents: `model: inherit`
- Python, Rust, Elixir-Phoenix, C++/Qt: `model: sonnet`
- **Recommendation**: Standardize or document rationale for model selection

##### Data Validation Libraries
- Python: **Pydantic2** (explicitly: "ALWAYS use Pydantic2, never dataclasses")
- TypeScript: **Zod** for runtime validation
- Java/Kotlin: No equivalent mandated
- **Recommendation**: Add runtime validation library recommendations for all typed languages

##### Testing Framework Specificity
- Some agents prescribe exact frameworks (Python: pytest, Ruby: RSpec)
- Others are more flexible (Java: mentions JUnit 5 + Mockito + AssertJ but less rigid)
- **Recommendation**: Strike balance between prescription and flexibility

#### Missing Elements in Some Agents

| Element | Present In | Missing From |
|---------|------------|--------------|
| Explicit anti-patterns list | Java, Rust, Swift | Python, TypeScript, Go |
| Self-correction mechanisms | Elixir | Most others |
| Output format expectations | Elixir, Java | Most others |
| Decision-making framework | C#, Kotlin | Most others |
| Performance guidance | Clojure, Swift | Most others |

### Recommendations for Unification

#### 1. Create a Base Template

Extract common sections into a template that all agents inherit:
- Engineering Principles (identical text)
- Code Review Philosophy
- Escalation Strategy
- Workflow Patterns
- Quality Gate Structure (technology fills in specific tools)

#### 2. Adopt Structural Patterns from Outliers

Evaluate adopting these patterns found in individual agents:

| Pattern | Source Agent | Recommendation |
|---------|--------------|----------------|
| Explicit workflow subsections | Java | Adopt — clearer guidance for different contexts |
| Self-correction mechanisms | Elixir | Adopt — valuable metacognitive prompts |
| Self-verification checklist | C# | Adopt — ensures completeness before presenting work |
| Anti-patterns section | Java, Rust, Swift | Adopt — explicit "don't do this" is valuable |
| Ecosystem split (language vs. framework) | Elixir/Phoenix | Consider for Python, TypeScript, Ruby |

#### 3. Standardize Optional Sections Checklist

Create a checklist of sections each agent should consider including:
- [ ] Anti-patterns to avoid
- [ ] Self-correction mechanisms
- [ ] Self-verification steps
- [ ] Decision-making framework
- [ ] Output format expectations

#### 4. Consider Ecosystem Splits

For ecosystems where the framework fundamentally changes the development context:
- `python-craftsperson` (libraries, CLI, pure Python)
- `python-django-craftsperson` (Django web apps, ORM, templates)
- `typescript-craftsperson` (Node.js, libraries)
- `typescript-react-craftsperson` (React apps, component patterns)

#### 5. Address Coverage Gaps

##### Missing Frontend Framework Agents

We currently have `typescript-craftsperson` but lack framework-specific variants:

| Gap | Would Cover |
|-----|-------------|
| `typescript-react-craftsperson` | React components, hooks, effects, state management |
| `typescript-vue-craftsperson` | Vue components, composables, reactivity |
| `typescript-angular-craftsperson` | Angular modules, services, RxJS patterns |
| `typescript-svelte-craftsperson` | Svelte components, stores, reactivity |

##### Frontend Concerns: Common vs. Framework-Specific

Frontend agents would share **common concerns**:
- Tailwind CSS v4 (mandated for all frontend work)
- Accessibility (WCAG compliance, semantic HTML)
- Responsive design patterns
- Dark mode / theming
- Performance (bundle size, lazy loading, Core Web Vitals)
- Browser compatibility

But have **framework-specific technical concerns**:

| Framework | Unique Technical Concerns |
|-----------|--------------------------|
| React | Hooks rules, effects cleanup, memo/callback optimization, RSC vs client |
| Vue | Composition API, reactivity caveats, provide/inject |
| Angular | Dependency injection, RxJS operators, change detection |
| Svelte | Reactive statements, stores, compiled output |
| Phoenix LiveView | Server state, push events, hooks, HEEx templates |

**Example**: All frontend agents would mandate Tailwind v4, but:
- React agent would cover `useEffect` cleanup and React Server Components
- Vue agent would cover `ref()` vs `reactive()` and `watchEffect`
- Phoenix agent would cover LiveView lifecycle and `phx-` bindings

This mirrors the existing `elixir-craftsperson` / `elixir-phoenix-craftsperson` split pattern.

#### 6. Add Missing Cross-Cutting Concerns

Some concerns appear inconsistently:
- **Observability**: Logging, metrics, tracing — missing from all agents
- **Accessibility**: Only in Phoenix agent — should be in all UI-related agents
- **Performance profiling**: Ad-hoc mentions — could be standardized

#### 7. Normalize Model Selection

Currently inconsistent (`sonnet` vs `inherit`). Either:
- Standardize all to `inherit`
- Document rationale for when `sonnet` is appropriate

### Agent Inventory

| Agent | Lines | Language/Framework | Model | Notable Features |
|-------|-------|-------------------|-------|------------------|
| python-craftsperson | 316 | Python | sonnet | Pydantic2 mandate |
| typescript-craftsperson | 431 | TypeScript/Node | sonnet | Zod validation, branded types |
| java-craftsperson | 228 | Java/Maven/Gradle | inherit | Verbose workflow, anti-patterns |
| kotlin-craftsperson | 234 | Kotlin/Ktor/Spring | inherit | Server-side focus |
| kotlin-android-craftsperson | ~250 | Kotlin/Android | inherit | Module architecture diagrams |
| go-craftsperson | ~200 | Go | inherit | Table-driven tests, channels |
| rust-craftsperson | ~200 | Rust | sonnet | Zero clippy warnings mandate |
| csharp-craftsperson | ~200 | C#/.NET | inherit | Roslyn analyzers |
| swift-craftsperson | ~300 | Swift/SwiftPM | inherit | DocC, value types emphasis |
| ruby-craftsperson | ~200 | Ruby/Rails | inherit | Capybara, Brakeman |
| elixir-craftsperson | 258 | Elixir/OTP | sonnet | Pure Elixir focus |
| elixir-phoenix-craftsperson | 802 | Phoenix/LiveView | sonnet | UI/dark mode, longest agent |
| clojure-craftsperson | 288 | Clojure | inherit | REPL-driven, data-oriented |
| cpp-qt-craftsperson | 395 | C++/Qt | sonnet | Memory safety, sanitizers |
