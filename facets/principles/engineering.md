---
name: engineering
facet: principles
scope: "Core engineering principles — Simple Design Heuristics, YAGNI, functional core/imperative shell, composition"
does-not-cover: "Language-specific idioms, toolchain commands, testing frameworks — see language and toolchain facets"
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---

## Engineering Principles (Your North Star)

**Code is Communication**
Every line you write optimizes for the next human reader. Variable names reveal intent, function signatures document contracts, module boundaries reflect domain concepts.

**Simple Design Heuristics** (in priority order):
1. **All tests pass** — Correctness is non-negotiable. Never compromise on passing tests.
2. **Reveals intent** — Code should read like an explanation. Prefer descriptive names over abbreviations.
3. **No knowledge duplication** — Avoid multiple spots that must change together for the same reason. Identical code is fine if it represents independent decisions that might diverge.
4. **Minimal entities** — Remove unnecessary indirection. Don't create abstractions until you need them.

When these heuristics conflict with user requirements, explicitly surface the tension and consult the user.

**Small, Safe Increments**
- Make single-reason commits that could ship independently
- Avoid speculative work (YAGNI — You Aren't Gonna Need It)
- Build the simplest thing that could work, then refactor

**Tests Are the Executable Spec**
- Write tests first (red) to clarify what you're building
- Make them pass (green) with the simplest implementation
- Tests verify behavior, not implementation details
- Only mock gateway/boundary interfaces, never mock library internals — if you need to mock a third-party library, wrap it in a gateway first
- Do not test gateway (I/O isolating) modules unless they have custom logic, and if they do favour moving that logic into the core

**Functional Core, Imperative Shell**
- Isolate pure business logic in the core (no side effects, easy to test)
- Push I/O, state changes, and side effects to the shell boundaries
- **Gateway Pattern**: All external interactions (filesystem, databases, APIs) go through gateway interfaces that can be mocked in tests. Never mock library internals — only mock gateway interfaces. Gateway modules should be thin wrappers around the underlying libraries, and should have no logic to test.
- Core functions should be pure: same inputs always produce same outputs

**Compose Over Inherit**
- Favour composition and interface-based polymorphism over inheritance
- Use contracts/interfaces for defining boundaries, not for code reuse
- Prefer pure functions; contain side effects at boundaries
