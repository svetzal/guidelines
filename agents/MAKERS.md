# Creating Your Own Craftsperson Agent

This guide helps you create a custom craftsperson agent that reinforces *your* project's standards, tools, and conventions. Use this when you have established opinions about how your codebase should be built and want an AI agent that consistently enforces them.

## Why Create a Custom Agent?

Our pre-built craftsperson agents are opinionated—they mandate specific tools (pytest, Pydantic2, ruff) and patterns. If your project:

- Uses different tools (unittest instead of pytest, mypy instead of ruff)
- Has established architectural patterns the team follows
- Has coding conventions documented in style guides
- Uses frameworks our agents don't cover (Django, FastAPI, NestJS)

...then a custom agent will serve you better than adapting to our opinions.

## The Agent Definition Pattern

Every craftsperson agent follows this structure. Copy this skeleton and fill in your specifics:

```markdown
---
name: your-project-craftsperson
description: When to invoke this agent with examples...
model: inherit
---

# Core Identity
Brief statement of expertise and mission.

# Engineering Principles
Your team's north star values (we recommend keeping ours—they're universal).

# Quality Assurance Process
Your mandatory quality gates—the checks that MUST pass.

# Language/Framework Guidelines
Idioms, patterns, and conventions specific to your stack.

# Workflow Patterns
How work flows from requirement to commit.

# Code Review Philosophy
How feedback is given (we recommend keeping the psychological safety framing).

# Escalation Strategy
When to consult the human.
```

## Step-by-Step: Extract Standards from Your Code

### Step 1: Audit Your Quality Gates

Look at your CI pipeline. What checks must pass before merge?

```bash
# Example: Extract from GitHub Actions, GitLab CI, or scripts
cat .github/workflows/ci.yml
cat Makefile
cat package.json | jq '.scripts'
```

Document every check as a mandatory gate:

```markdown
## Quality Assurance Process

Before considering any code complete, you **MUST** complete all steps:

1. **Run Tests** — `make test` must pass with zero failures
2. **Type Checking** — `mypy src/` with zero errors
3. **Linting** — `flake8 src/` with zero warnings
4. **Formatting** — `black --check src/` must pass
5. **Security** — `safety check` for dependency vulnerabilities
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
  api/             # FastAPI routes (thin, delegate to domain)
  config/          # Environment and settings
tests/
  unit/            # Fast, isolated, mock adapters
  integration/     # Real database, real services
```

### Dependency Direction
- `api/` depends on `domain/` and `adapters/`
- `domain/` has NO external dependencies
- `adapters/` implement interfaces defined in `domain/`
```

### Step 3: Capture Your Idioms and Conventions

Review recent PRs and code reviews. What feedback recurs?

Look for:
- Naming conventions (snake_case, PascalCase, prefixes)
- Error handling patterns (exceptions, result types, error codes)
- Logging conventions
- Testing patterns (fixtures, factories, mocking approach)
- Documentation requirements

```markdown
## Coding Conventions

### Naming
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `SCREAMING_SNAKE_CASE`
- Private: prefix with `_`

### Error Handling
- Use custom exception hierarchy rooted at `AppError`
- Never catch bare `Exception`
- Always log errors with context before re-raising

### Testing
- Use pytest fixtures for setup
- Factory functions in `tests/factories.py`
- Mock external services with `responses` library
- Test file mirrors source: `src/foo/bar.py` → `tests/unit/foo/test_bar.py`
```

### Step 4: Identify Your Tool Stack

Be explicit about versions and configurations:

```markdown
## Tool Stack

| Purpose | Tool | Version | Config |
|---------|------|---------|--------|
| Runtime | Python | 3.11+ | - |
| Testing | pytest | 7.x | `pyproject.toml` |
| Types | mypy | 1.x | `mypy.ini` |
| Linting | ruff | 0.1.x | `ruff.toml` |
| Formatting | black | 23.x | `pyproject.toml` |
| Dependencies | poetry | 1.7+ | `pyproject.toml` |
```

### Step 5: Document Anti-Patterns

What do code reviewers consistently reject? Make these explicit:

```markdown
## Anti-Patterns to Avoid

- **God objects**: Classes with more than ~200 lines or 10+ methods
- **Nested callbacks**: More than 2 levels of nesting in async code
- **Magic strings**: Use enums or constants for repeated strings
- **Implicit dependencies**: All dependencies must be injected
- **Print debugging**: Use structured logging, never `print()`
- **Commented-out code**: Delete it; git remembers
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

## Complete Example: Django Project Agent

Here's a complete custom agent for a Django project:

```markdown
---
name: acme-django-craftsperson
description: Use for all work on the ACME Django application...
model: inherit
---

You are the guardian of the ACME Django codebase. You ensure all code
follows our established patterns and passes our quality gates.

## Engineering Principles

[Keep the standard Simple Design Heuristics—they're universal]

## Quality Gates (MANDATORY)

1. **Tests**: `pytest --cov=acme --cov-fail-under=85`
2. **Types**: `mypy acme/`
3. **Lint**: `ruff check acme/`
4. **Format**: `ruff format --check acme/`
5. **Migrations**: `python manage.py makemigrations --check --dry-run`
6. **Security**: `bandit -r acme/` and `safety check`

## Architecture

### App Structure
- `acme/core/` — Shared utilities, base classes
- `acme/users/` — User management
- `acme/billing/` — Payment processing
- `acme/api/` — DRF serializers and viewsets

### Patterns
- Fat models, thin views
- Business logic in model methods or service modules
- Use `select_related`/`prefetch_related` proactively
- Signals only for cross-app communication

## Django Conventions

- Model fields: `snake_case`
- URL names: `app:action-resource` (e.g., `billing:create-invoice`)
- Templates: `app/resource_action.html`
- Always use `get_object_or_404`, never bare `Model.objects.get`

## Testing

- Fixtures in `conftest.py` using factory_boy
- Integration tests use `@pytest.mark.django_db`
- Mock external APIs with `responses`
- Test views through DRF's `APIClient`

## Anti-Patterns

- No raw SQL unless performance-critical and documented
- No `*` imports
- No logic in migrations
- No business logic in serializers
```

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
- [ ] **Engineering Principles**: Values that guide decisions
- [ ] **Quality Gates**: Mandatory checks with exact commands
- [ ] **Architecture**: Project structure, dependency rules
- [ ] **Conventions**: Naming, error handling, logging, testing
- [ ] **Tool Stack**: Versions, configurations
- [ ] **Anti-Patterns**: Explicit "don't do this" list
- [ ] **Self-Correction**: Metacognitive prompts
- [ ] **Workflow**: How work flows from requirement to commit
- [ ] **Code Review Philosophy**: How feedback is framed
- [ ] **Escalation**: When to ask the human
