# Creating Your Own Craftsperson Agent

This guide helps you create a custom craftsperson agent that reinforces *your* project's standards, tools, and conventions. Use this when you have established opinions about how your codebase should be built and want an AI agent that consistently enforces them.

## Why Create a Custom Agent?

Pre-built craftsperson agents are opinionated — they mandate specific tools and patterns. Build a custom one when your repo has established standards (tooling, architecture, CI gates, security posture) that the agent must enforce.

## The Agent Definition Pattern

Every craftsperson agent follows this structure. Copy this skeleton and fill in your specifics:

```markdown
---
name: your-project-craftsperson
description: |
  When to invoke this agent (with examples).
  Include what the agent MUST preserve and must NOT change unless explicitly authorized.
model: inherit
---

# Core Identity
Brief statement of expertise and mission.

# Invariant Preservation Contract
What the agent must detect and preserve (see below).

# Engineering Principles
Your team's north star values (we recommend keeping ours—they're universal).

# Quality Assurance Process
Your mandatory quality gates—the checks that MUST pass, with exact commands.

# Language/Framework Guidelines
Idioms, patterns, and conventions specific to your stack.

# Workflow Patterns
How work flows from requirement to commit.

# Code Review Philosophy
How feedback is given (we recommend keeping the psychological safety framing).

# Escalation Strategy
When to consult the human.
```

## Invariant Preservation Contract (non-negotiable)

Your agent MUST detect and preserve:

- **Toolchain/version constraints**: runtime version, compiler/VM/toolchain version, lockfiles, package manager choice
- **Public API and compatibility promises**: semver rules, migration paths, deprecation policies
- **Feature flag / build profile semantics**: default features, conditional compilation, build configurations
- **Security gates and policy decisions**: dependency sources, license policies, audit/signoff requirements, vulnerability scanning tools
- **Architectural boundaries**: module structure, dependency direction, I/O isolation patterns

If the agent believes one of these must change, it MUST stop and ask the user before proceeding. This prevents accidental toolchain bumps, API breaks, and policy drift.

## Step-by-Step: Extract Standards from Your Code

### Step 1: Audit Your Quality Gates

Look at your CI pipeline. What checks must pass before merge?

```bash
# Extract from CI workflows or scripts
cat .github/workflows/ci.yml
cat Makefile
```

Document every check as a mandatory gate, with exact commands that can run locally and in CI:

```markdown
## Quality Assurance Process

Before considering any code complete, you **MUST** complete all steps:

1. **Formatting** — `<format-check-command>` must pass
2. **Linting** — `<lint-command>` with zero warnings
3. **Type Checking** — `<type-check-command>` with zero errors
4. **Tests** — `<test-command>` must pass with zero failures
5. **Security** — `<dependency-scan-command>` for vulnerability scanning
6. **Docs** — `<doc-build-command>` must build cleanly
```

### Step 2: Document Your Architectural Patterns

Look at your codebase structure. What patterns are consistent?

Questions to answer:
- How is the codebase organized? (by feature, by layer, by domain)
- What's the directory structure convention?
- How do modules/packages communicate?
- Where does business logic live vs. I/O?

```markdown
## Architectural Patterns

### Project Structure
```
src/
  domain/          # Pure business logic, no I/O
  adapters/        # Database, HTTP, external services
  api/             # Routes/handlers (thin, delegate to domain)
  config/          # Environment and settings
tests/
  unit/            # Fast, isolated, mock adapters
  integration/     # Real dependencies
```

### Dependency Direction
- API layer depends on domain and adapters
- Domain has NO external dependencies
- Adapters implement interfaces defined in domain
```

### Step 3: Capture Your Idioms and Conventions

Review recent PRs and code reviews. What feedback recurs?

Look for:
- Naming conventions
- Error handling patterns
- Logging conventions
- Testing patterns (fixtures, factories, mocking approach)
- Documentation requirements

```markdown
## Coding Conventions

### Naming
- Types: `PascalCase`
- Functions/variables: language-appropriate casing
- Constants: `SCREAMING_SNAKE_CASE`

### Error Handling
- Use the project's established error type hierarchy
- Preserve error context at every level
- Handle errors at appropriate boundaries

### Testing
- Use the project's test framework and conventions
- Test file organization mirrors source structure
- Mock only at boundary/gateway traits
```

### Step 4: Identify Your Tool Stack

Be explicit about versions, configurations, and where each tool is configured:

```markdown
## Tool Stack

| Purpose | Tool | Version/Policy | Config location |
|---------|------|----------------|-----------------|
| Runtime | `<language>` | `<version constraint>` | `<config file>` |
| Testing | `<test tool>` | `<version>` | `<config file>` |
| Linting | `<linter>` | `<version>` | `<config file>` |
| Formatting | `<formatter>` | `<version>` | `<config file>` |
| Security | `<scanner>` | `<version>` | `<config file>` |
| Dependencies | `<pkg manager>` | `<version>` | `<config file>` |
```

### Step 5: Document Anti-Patterns

What do code reviewers consistently reject? Make these explicit:

```markdown
## Anti-Patterns to Avoid

- **God objects**: Classes/modules with too many responsibilities
- **Deep nesting**: More than 2-3 levels of nesting
- **Magic values**: Use named constants or enums for repeated values
- **Implicit dependencies**: All dependencies must be injected or explicit
- **Commented-out code**: Delete it; version control remembers
```

### Step 6: Add Self-Correction Prompts

Help the agent catch itself making mistakes:

```markdown
## Self-Correction

When you catch yourself:
- Writing a function > 20 lines → Extract smaller functions
- Adding a parameter to fix one case → Consider if design is wrong
- Copying code → Extract shared abstraction
- Writing a comment explaining "what" → Rename to make it obvious
- Mocking more than 2 dependencies → Test is probably too integrated
```

## Complete Example: Template-Only Agent (placeholders)

This example uses placeholders to demonstrate the agent shape without prescribing any specific language or framework:

```markdown
---
name: acme-craftsperson
description: |
  Use for all work on the ACME application. Enforces our quality gates,
  architectural patterns, and coding conventions.

  Invariants to preserve: runtime version, dependency lockfile, public API
  contracts, feature flag semantics.
model: inherit
---

You are the guardian of the ACME codebase. You ensure all code
follows our established patterns and passes our quality gates.

## Invariant Preservation

Detect and preserve:
- Runtime/compiler version constraint (see <config-file>)
- Dependency lockfile (do not regenerate without authorization)
- Public API contracts (no breaking changes without explicit approval)
- Feature flag defaults (do not change without authorization)

## Engineering Principles

[Keep the standard Simple Design Heuristics—they're universal]

## Quality Gates (MANDATORY)

1. **Format**: `<format-check-command>`
2. **Lint**: `<lint-command>`
3. **Test**: `<test-command>`
4. **Type Check**: `<type-check-command>`
5. **Security**: `<security-scan-command>`
6. **Docs**: `<doc-build-command>`

## Architecture

### Module Structure
- `<module>/core/` — Pure business logic, no I/O
- `<module>/adapters/` — External service wrappers (gateways)
- `<module>/api/` — Thin entry points, delegate to core

### Patterns
- Functional core, imperative shell
- Gateway traits at I/O boundaries
- Dependency injection for testability

## Conventions

- [Naming conventions for your language]
- [Error handling patterns for your stack]
- [Logging and observability standards]

## Testing

- Unit tests for pure logic (functional core)
- Integration tests for boundary wiring
- Mock only gateway traits, never internals
- [Framework-specific test patterns]

## Anti-Patterns

- [List what your team consistently rejects in code review]
```

## Language-Specific Craftsperson Agents

Keep MAKERS language-agnostic. Create separate language/framework agents that inherit this structure and add language-specific enforcement (toolchain, idioms, ecosystem conventions).

Pre-built agents available:
- `rust-craftsperson`
- `python-craftsperson`
- `uv-python-craftsperson`
- `java-craftsperson`
- `csharp-craftsperson`
- `kotlin-craftsperson`
- `kotlin-android-craftsperson`
- `go-craftsperson`
- `swift-craftsperson`
- `ruby-craftsperson`
- `typescript-craftsperson`
- `elixir-craftsperson`
- `elixir-phoenix-craftsperson`
- `clojure-craftsperson`
- `cpp-qt-craftsperson`

Use these as references when building your own, or customize them for your project's specific tooling and conventions.

## Validating Your Agent

Before deploying your custom agent:

1. **Test against recent PRs** — Would the agent have caught issues reviewers found?
2. **Run on existing code** — Does it flag things you'd actually want fixed?
3. **Check for conflicts** — Do any rules contradict each other?
4. **Get team review** — Does the team agree these are the standards?

## Evolving Your Agent

Your agent should evolve with your codebase:

- **After incidents**: Add rules to prevent recurrence
- **After team decisions**: Update when conventions change
- **After tool changes**: Update quality gates when tooling evolves
- **Quarterly review**: Is the agent still reflecting reality?

## Sharing with Your Team

Place your agent definition where your team can find and invoke it:

```
.claude/agents/acme-craftsperson.md
```

Or in a central guidelines repository that team members reference.

---

## Quick Reference: Section Checklist

Use this checklist when creating your agent:

- [ ] **Frontmatter**: name, description with examples, model
- [ ] **Core Identity**: One paragraph establishing expertise
- [ ] **Invariant Preservation**: What must not change without authorization
- [ ] **Engineering Principles**: Values that guide decisions
- [ ] **Quality Gates**: Mandatory checks with exact commands
- [ ] **Architecture**: Project structure, dependency rules
- [ ] **Conventions**: Naming, error handling, logging, testing
- [ ] **Tool Stack**: Versions, configurations, config file locations
- [ ] **Anti-Patterns**: Explicit "don't do this" list
- [ ] **Self-Correction**: Metacognitive prompts
- [ ] **Workflow**: How work flows from requirement to commit
- [ ] **Code Review Philosophy**: How feedback is framed
- [ ] **Escalation**: When to ask the human
