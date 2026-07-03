# Application Conventions

This is the gathering place for **application-level design conventions** — the patterns that make our software feel like it came from one author, regardless of language or toolchain.

Where `facets/` holds universal engineering principles (composed into every craftsperson agent) and `skills/` holds runtime toolchain guidance, conventions sit in between: they apply to a *kind* of application (a CLI tool, a daemon, a web service), not to every project and not to a specific toolchain.

## Lifecycle

Conventions start as plain documentation, mature through use in design and review conversations, and graduate into skills once the guidance is stable enough to direct agent work:

1. **Draft** — a convention document here, refined by reviewing real tools against it.
2. **Review practice** — the document is used as the rubric for UX/design reviews of existing tools; findings feed back into the document.
3. **Skill** — stable conventions get distilled into a runtime skill (e.g. a `cli-ux-review` skill) loaded when the project context matches.

## Documents

- [cli-ux.md](cli-ux.md) — UX principles for command-line tools
