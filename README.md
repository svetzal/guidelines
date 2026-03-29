# Agentic Engineering Guidelines

Guardrails for AI-assisted software development — a collection of agents, skills, and quality guidance that keep agentic coding tools productive and consistent.

## What's Here

- **`agents/`** — Opinionated "craftsperson" agents for 16 language/framework stacks. Each agent enforces quality gates, TDD workflow, and language-idiomatic patterns. See [agents/README.md](agents/README.md).
- **`skills/`** — Reusable skills following the [Agent Skills specification](https://agentskills.io/specification). See [skills/README.md](skills/README.md).
- **`AGENTS.md`** — Baseline standards (versioning, frontmatter, file conventions) shared by all agents and skills in this repo.

## Why This Exists

AI coding agents are powerful but unconstrained — they'll happily skip tests, ignore linters, invent abstractions nobody asked for, and commit without running quality checks. These guidelines give agents a clear set of engineering principles to follow:

- **Quality gates** — tests, linting, formatting, and security scans must pass before work is done
- **Simple Design Heuristics** — tests pass, reveals intent, no knowledge duplication, minimal entities
- **Functional core / imperative shell** — pure logic at the center, I/O at the boundaries
- **TDD workflow** — red, green, refactor
- **Documentation sync** — docs stay aligned with code

## Getting Started

Copy or symlink the agents and skills you need into your project's agentic tool configuration. Each agent is a standalone `.md` file; each skill is a self-contained directory with a `SKILL.md`.

For details on creating your own agents, see [agents/MAKERS.md](agents/MAKERS.md).

## Author

Stacey Vetzal — stacey@vetzal.com
