This is a collection of custom agents, skills, and general guidance written by Stacey Vetzal (stacey@vetzal.com).

## Baseline Quality Guidance

Standards that apply to both agents and skills in this repository.

### Frontmatter Metadata

Use the `metadata` field for versioning and authorship. This follows the
[Agent Skills specification](https://agentskills.io/specification) and keeps
frontmatter portable across agent platforms.

```yaml
metadata:
  version: "1.3.1"
  author: Stacey Vetzal
```

Write multi-line descriptions as YAML block scalars. Do not store line breaks
as literal `\n` sequences in an unquoted scalar. Colons in that form can make
the frontmatter invalid, which prevents package managers from reading the
version even when `metadata.version` is present.

```yaml
description: |
  Use this agent when working with the example tool.

  Invoke it after a logical chunk of work is complete.
```

**Version** — use semantic versioning (`MAJOR.MINOR.PATCH`):
- **MAJOR**: Breaking changes to behavior or removed guidance
- **MINOR**: New capabilities, sections, or recommendations
- **PATCH**: Corrections, clarifications, wording improvements

**Author** — use a human-readable name, not an org handle or email.

### Version Bumps on Commit

When committing changes to an agent or skill, bump its `metadata.version`
as part of the same commit. Choose the increment based on what changed:

- **PATCH** for corrections, typo fixes, clarifications
- **MINOR** for new sections, added tooling recommendations, expanded guidance
- **MAJOR** for removed sections, changed behavior, or anything that would
  break workflows relying on the previous version

Do not batch version bumps — each agent or skill modified in a commit should
have its own version incremented independently.

### Model Tags

**Avoid `model:` in frontmatter.** Model names are platform-specific and do
not transfer across agent implementations:

| Platform    | Example model value        | Meaning                        |
|-------------|----------------------------|--------------------------------|
| Claude Code | `sonnet`                   | Latest Sonnet (currently 4.6)  |
| Copilot     | `gpt-4o`, `claude-sonnet`  | Specific model family          |
| Codex       | `o3`, `o4-mini`            | OpenAI reasoning models        |
| Cursor      | `claude-3.5-sonnet`        | Pinned model version           |

Problems with `model:` tags:
- **Not portable** — `sonnet` means nothing to Codex; `o3` means nothing to Claude
- **Implicit version drift** — `sonnet` silently upgrades when Anthropic releases a new Sonnet, which may change agent behavior
- **No graceful fallback** — platforms that don't recognize the value may error or silently ignore it

If you must specify a model (e.g., a skill that requires a large context window
or specific capabilities), document the *requirement* in `compatibility` instead:

```yaml
compatibility: Requires a model with 100k+ context window
```

This lets each platform choose an appropriate model rather than hard-coding one
that only works in a single ecosystem.

### Directory and File Conventions

- Agent files live in `agents/` as individual `.md` files
- The agent `name` frontmatter field must match its filename (without `.md`)
  e.g., `name: typescript-craftsperson` lives in `typescript-craftsperson.md`
- Skills live in `skills/` as directories containing a `SKILL.md`
- The skill `name` frontmatter field must match its parent directory name
- See [agents/README.md](agents/README.md) and [skills/README.md](skills/README.md) for format details

## Validators

Intent records under `intents/` may carry `static-check` evidence entries that
name an executable validator. The validators live in `checks/` beside the
records they serve: `checks/<language>/<slug>.py` is the entry point, the checks
themselves are in `checks/lib/adherence/`, and `checks/README.md` documents the
layout and the helper-binary convention. The invocation protocol and verdict
contract are owned by the verifier, `cmv`, and specified in `CMV.md` of the
context-mixer repository (https://github.com/svetzal/context-mixer2); this
repository implements that protocol, it does not define it.

Every validator ships with a fixture it is expected to pass and one it is
expected to not pass, under `checks/fixtures/<language>/`, and the calibration
gate runs all of them the way the verifier would, twice, requiring identical
output:

```bash
python3 checks/calibrate.py
```

A validator change — a new check, a corrected one, a changed helper — is not
done until calibration is green. Add the fixture that demonstrates the
correction in the same commit.
