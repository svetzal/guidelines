# Agent Skills Guide

Standards and structure for skills in this repository, based on the
[Agent Skills specification](https://agentskills.io/specification).

## Directory Structure

Each skill is a folder containing at minimum a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation loaded on demand
├── baselines/        # Optional: baseline configs, schemas, templates
└── assets/           # Optional: static resources (images, data files)
```

The folder name **must match** the `name` field in the SKILL.md frontmatter.

## SKILL.md Frontmatter

### Required Fields

| Field         | Constraints                                                          |
|---------------|----------------------------------------------------------------------|
| `name`        | 1-64 chars. Lowercase `a-z`, digits, hyphens only. No leading/trailing/consecutive hyphens. Must match directory name. |
| `description` | 1-1024 chars. Describe what the skill does **and when to use it**. Include trigger keywords. |

### Optional Fields

| Field           | Purpose                                                                |
|-----------------|------------------------------------------------------------------------|
| `license`       | License name or reference to a bundled LICENSE file.                   |
| `compatibility` | Environment requirements (runtime, system packages, network). Max 500 chars. |
| `metadata`      | Arbitrary key-value map for additional properties.                     |
| `allowed-tools` | Space-delimited list of pre-approved tools. (Experimental)             |

### Versioning

The spec does not define a top-level `version` field. Use `metadata` for versioning:

```yaml
metadata:
  version: "1.0"
  author: example-org
```

Some of our existing skills use a top-level `version` field outside the spec.
Going forward, prefer `metadata.version` for portability across agent products.

### Minimal Example

```yaml
---
name: my-skill
description: Does X when user asks for Y.
---
```

### Full Example

```yaml
---
name: pdf-processing
description: >
  Extract PDF text, fill forms, merge files. Use when handling PDFs
  or when the user mentions PDFs, forms, or document extraction.
license: Apache-2.0
compatibility: Requires Python 3.12+ and uv
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(uv:*) Read
---
```

## Writing Good Descriptions

The `description` is the **sole trigger mechanism** -- agents load only `name` and
`description` at startup and decide whether to activate the skill based on them.

- **Use imperative phrasing**: "Use this skill when..." not "This skill does..."
- **Focus on user intent**: describe what the user is trying to achieve
- **Be pushy**: explicitly list contexts, including non-obvious ones
- **Include trigger keywords**: mention synonyms and phrasings users might use
- **Stay under 1024 chars**: long enough for scope, short enough to not bloat context

## SKILL.md Body

The markdown body contains instructions the agent follows after activation.
Keep `SKILL.md` under **500 lines / ~5000 tokens**. Move detailed reference
material to separate files.

### Recommended Sections

1. **Step-by-step instructions** -- the core workflow
2. **Gotchas** -- environment-specific facts that defy reasonable assumptions
3. **Examples** -- concrete input/output pairs

### Effective Instruction Patterns

- **Add what the agent lacks, omit what it knows.** Don't explain HTTP or what a
  PDF is. Focus on project-specific conventions and non-obvious edge cases.
- **Provide defaults, not menus.** Pick one tool/approach as the default; mention
  alternatives briefly.
- **Favor procedures over declarations.** Teach *how to approach* a class of
  problems, not *what to produce* for a specific instance.
- **Match specificity to fragility.** Be prescriptive for fragile operations
  (exact commands, exact sequences). Give freedom where multiple approaches work.
- **Validation loops.** Instruct the agent to validate its own work before
  proceeding: do the work, run a check, fix issues, repeat.
- **Templates for output format.** Provide concrete structural templates rather
  than describing formats in prose.

## Progressive Disclosure

Skills use three tiers of context:

1. **Metadata** (~100 tokens) -- `name` + `description`, loaded at startup for all skills
2. **Instructions** (<5000 tokens) -- full `SKILL.md` body, loaded on activation
3. **Resources** (as needed) -- files in `scripts/`, `references/`, etc., loaded on demand

Tell the agent **when** to load each resource file:
"Read `references/api-errors.md` if the API returns a non-200 status code"
is better than a generic "see references/ for details."

## Scripts

### Self-Contained Scripts

Bundle reusable logic in `scripts/` with inline dependency declarations:

- **Python**: PEP 723 inline metadata, run with `uv run scripts/foo.py`
- **JavaScript/TypeScript**: use `npx`, `bunx`, or Deno `npm:` specifiers
- **Go**: `go run package@version`

Pin dependency versions for reproducibility.

### Script Design for Agents

- **No interactive prompts** -- agents run in non-interactive shells
- **`--help` flag** -- primary way the agent learns the script's interface
- **Helpful error messages** -- say what went wrong, what was expected, what to try
- **Structured output** -- prefer JSON/CSV over free-form text; data to stdout, diagnostics to stderr
- **Idempotent** -- agents may retry; "create if not exists" over "create and fail on duplicate"
- **Safe defaults** -- destructive operations should require explicit `--confirm`/`--force` flags

### Referencing Scripts

Use relative paths from the skill directory root:

```markdown
Run the extraction script:
```bash
bash scripts/validate.sh "$INPUT_FILE"
```
```

## Iterating on Skills

1. **Start from real expertise** -- extract from a hands-on task or synthesize
   from project artifacts (runbooks, code reviews, incident reports)
2. **Refine with real execution** -- run against real tasks, read execution
   traces, revise instructions based on what the agent actually does
3. **Test descriptions** -- design eval queries (should-trigger and
   should-not-trigger) and measure trigger rates across multiple runs
4. **Keep gotchas current** -- when the agent makes a mistake you correct,
   add the correction to the gotchas section
