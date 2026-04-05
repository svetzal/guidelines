# Faceted Agent Composition

Facets are the authoring-time building blocks of craftsperson agents. Each facet captures a single, independent concern — a language's idioms, a set of engineering principles, a testing pattern. Recipes compose facets into the monolithic agent `.md` files that LLM consumers actually use.

## The Two-Layer Model: Agents + Skills

Engineering intent splits into two layers with different lifecycles:

**Agents (composed from facets at authoring time):**
- Universal engineering principles
- Language-specific idioms (type system, error handling, async patterns)
- Testing patterns (BDD-style, table-driven, etc.)

**Skills (loaded at runtime based on project context):**
- Toolchain guidance (uv, pip, bun, npm, cargo, mix)
- Quality gate commands (tool-specific invocations)
- Framework patterns (Phoenix LiveView, React, etc.)

This separation means a single `python-craftsperson` agent works with *either* uv or pip — Claude detects `uv.lock` and loads the `uv` skill, or falls back to the `pip` skill. No more separate `uv-python-craftsperson` agent.

## Why Facets?

The 16 craftsperson agents in `agents/` contain massive duplication:
- ~200 lines of engineering principles are **identical text** across all 16
- Language idioms are unique per language but shared across toolchain variants

Facets eliminate this duplication at authoring time. A change to engineering principles is made once in `facets/principles/engineering.md` and flows to all assembled agents.

## Directory Structure

```
guidelines/
  facets/
    principles/           # Universal — always included in every agent
      engineering.md       # Simple Design Heuristics, YAGNI, functional core/imperative shell
      code-review.md       # Collaboration mindset, psychological safety
      self-correction.md   # Metacognitive checks
      escalation.md        # When to consult the user
      output-expectations.md
    language/             # Pick one per recipe
      python.md            # Python idioms, type hints, async, Pydantic2
      (future: elixir.md, rust.md, go.md, typescript.md, ...)
    testing/              # Per language testing pattern
      pytest-bdd.md        # Describe*/should_* BDD-style spec tests
      (future: exunit-mox.md, cargo-test.md, ...)
    recipes/              # Composition declarations
      python-craftsperson.json
  skills/                 # Runtime-loaded toolchain and framework guidance
    uv/SKILL.md           # uv project management + quality gates
    pip/SKILL.md          # pip dependency management + quality gates
    (future: bun/, npm/, cargo/, mix/, phoenix-liveview/, react/, ...)
```

## Facet Frontmatter

```yaml
---
name: python
facet: language
scope: "Python idioms, type hints, async patterns, Pydantic2"
does-not-cover: "Package management (see uv/pip skills), quality gate commands"
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---
```

## Recipes

A recipe declares which facets compose into an agent:

```json
{
  "name": "python-craftsperson",
  "produces": "agents/python-craftsperson.md",
  "facets": [
    "principles/engineering",
    "principles/code-review",
    "principles/self-correction",
    "principles/escalation",
    "principles/output-expectations",
    "language/python",
    "testing/pytest-bdd"
  ],
  "runtime_skills": [
    "uv — when uv.lock or .python-version present",
    "pip — when no uv.lock present"
  ]
}
```

The `runtime_skills` field documents which skills complement this agent. Skills are not baked into the agent — they are loaded by the LLM consumer at runtime when the project context matches.

## Agents vs Skills: When Each Applies

| Concern | Layer | Why |
|---------|-------|-----|
| Engineering principles | Agent (facet) | Universal, always active |
| Language idioms | Agent (facet) | Defines the craftsperson's expertise |
| Testing patterns | Agent (facet) | Tightly coupled to language |
| Toolchain (uv, pip, bun) | Skill | Runtime-contextual, project-dependent |
| Quality gate commands | Skill | Depend on toolchain choice |
| Framework patterns | Skill | Optional, project-dependent |
| Documentation tools | Skill | Depend on project setup |

## Migration Status

**Phase 1 (current):** Universal principles and Python facets extracted. Toolchain guidance (uv, pip) packaged as skills. The monolithic agents in `agents/` remain canonical.

**Phase 2 (next):** Extract language facets for remaining languages. Create toolchain skills for remaining ecosystems (bun, npm, cargo, mix).

**Phase 3:** Create framework skills (phoenix-liveview, react, fastapi). Eliminate `elixir-phoenix-craftsperson` as separate agent — becomes `elixir-craftsperson` + `phoenix-liveview` skill.

**Phase 4:** Validate by assembling all agents from facets and comparing against originals.

**Phase 5:** Monolithic agents become generated artifacts. `uv-python-craftsperson` retired in favor of `python-craftsperson` + `uv` skill.

## Relationship to Marketplace Plugins

The guidelines repo is a Claude marketplace plugin (`svetzal-guidelines`). Facets, agents, and skills all ship together:

```
.claude-plugin/
  marketplace.json        # Plugin registry
agents/                   # Assembled agents (consumer-facing)
skills/                   # Runtime skills (consumer-facing)
facets/                   # Authoring structure (maintainer-facing)
```

Consumers install agents and skills from the marketplace. Facets are internal to the authoring process — they are not installed or distributed directly.
