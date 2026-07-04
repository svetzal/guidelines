---
name: cli-ux
description: >
  Apply consistent, humane UX principles when designing, building, or reviewing command-line tools —
  command grammar and subcommands, verb and flag naming, plan/apply safety, human vs --json output,
  help text, error messages, install footprint, and client/daemon splits. Use this skill whenever the
  user is creating a new CLI tool or adding commands, flags, or output to an existing one; choosing
  verbs or flag names; designing a tool's --help, dry-run, confirmation, or error messages; or doing a
  UX/design review of a CLI's surface — even if they don't say "UX". Trigger on mentions of CLI design,
  subcommand structure, flag conventions, argparse/click/clap/cobra/oclif command surfaces, dry-run vs
  apply, --json output, shell completions, exit codes, or "review my CLI".
license: MIT
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---

# CLI UX

Command-line tools ask users to carry the interface in their heads. Every inconsistency — a flag that
means one thing here and another there, a verb that's `remove` in one tool and `delete` in the next —
taxes memory, and for people not yet comfortable at the command line it breeds fear. Apply these
principles so a family of tools feels like one author wrote them: learn one, and you've mostly learned
them all.

Use this skill in two modes:

- **Design/build** — when creating a CLI or adding commands, flags, or output. Reach for the principle
  that governs the decision (naming → §3/§4, mutations → §5, output → §6, errors → §8) and follow the
  established convention rather than inventing a marginally-different one.
- **Review** — when auditing an existing CLI's surface. Walk the tool with the workflow at the end and
  produce a findings list ordered by user pain.

## Three commitments that frame everything

- **Unix philosophy at a humane altitude.** Small composable programs — but composition doesn't force
  every program to be low-level. A domain of related commands under one installable executable
  (`git`, `docker`, `gh`) is still a small program to the shell: it pipes, it exits, it composes.
- **The user's memory is the scarcest resource.** Optimize for predictability over cleverness. The
  success condition is a user who *guesses* the right command without reading docs.
- **Every output teaches.** Deeper than `--help`: every line a tool prints — success confirmations,
  dry-run plans, errors, empty results — is concise *and* deepens the user's model of what just
  happened and what their world now looks like. The educational dry-runs (§5), help examples (§7), and
  next-step errors (§8) below are not separate niceties; they are this one stance applied deliberately.

## 1. Consistency beats cleverness

A fleet should feel single-authored. Before inventing a new verb, flag, or output shape, check whether
a sibling command or tool already has a convention — and follow it, even if you can imagine something
marginally better. Divergence needs a reason; convergence doesn't.

## 2. One domain, one executable

Group a domain's commands under a single binary with subcommands rather than scattering `tool-this`,
`tool-that` across PATH. One name to remember, one thing to install, one thing to uninstall. Keep the
hierarchy shallow: `tool verb` for small tools, `tool noun verb` for larger domains. Three levels deep
is a smell — the domain wants to split, or the grammar is fighting you.

## 3. A small, shared verb vocabulary

Use imperative base-form verbs and reuse the same ones everywhere: `add`, `list`, `show`, `edit`,
`remove`, `run`, `status`, `search`, `init`, `setup`. Never offer synonyms for one idea (`update` vs
`promote` vs `sync` forces the user to learn three fine distinctions), and never use one verb for
different ideas across tools. Kebab-case compound names (`check-quality`, `mark-duplicate`), never
underscores.

## 4. Flags are a shared vocabulary too

The same flag means the same thing in every command and every tool:

- `--json` — machine-readable output (see §6)
- `--apply` — execute a mutation that previews by default (see §5)
- `--yes` — skip confirmation prompts (the scriptability escape hatch)
- `--force` — override a safety *refusal*; never a synonym for `--yes`
- `--quiet` / `--verbose` — volume control
- Kebab-case always (`--dry-run`, never `--dry_run` — including in flag *values*)

In code, define flags once in a canonical options module and reuse them across commands — consistency
enforced by construction, not by review.

## 5. Safe by default: plan, then apply

Commands that mutate state show what *would* happen by default and require an explicit `--apply` to do
it. `--apply` is the standard — not `--write`, not `--commit`, not per-tool variants. The workflow is
the point: run the command, read the plan, hit up-arrow, append `--apply`. Dry run and real run are the
same command, so nothing is retyped or re-remembered, and the plan the user approved is exactly what
executes.

For that to be trustworthy, the dry run must *educate precisely*: name each concrete change — which
records, which files, which values, before and after — not a vague "would modify 3 items." A dry run
the user can't check against their intent is theater, not safety. Corollaries:

- Mark mutating commands in help text (e.g. `[Mutates]` / `[Mutates with --apply]`) so the read/write
  boundary is visible before anything runs.
- End dry-run output by telling the user how to proceed: "re-run with --apply to make these changes."
- Read-only commands must NOT carry `--dry-run` — a safety flag on a safe command teaches users the
  flag is meaningless.
- Confirmation prompts always have a `--yes` bypass; a prompt with no bypass makes the tool unusable in
  scripts.
- After a mutation, report what changed in countable terms ("categorized 14 transactions, 2 skipped").

## 6. Human output on the terminal, machine output on demand

Default output is for humans: tables, color, relative times. But every command that reports data also
accepts `--json` — a tool without machine output can't be composed, scripted, or watched by an agent.

- Data to stdout; progress, warnings, and chatter to stderr — so pipes carry data, not noise.
- Streams (logs, event feeds) emit JSONL, one object per line, jq-friendly.
- Detect the terminal: no color and no interactive prompts when stdout isn't a TTY; respect `NO_COLOR`.
- Exit codes are API: `0` success, nonzero distinguishes failure classes where callers care (e.g. a
  `doctor` exiting `2` for "actionable issues found").

## 7. Help is the front door

Most users meet a tool through `--help`, not the README. Every command's help carries a one-line
summary and at least one realistic, copy-pasteable example. Top-level help reads as a scannable map of
the domain. Ship shell completions enabled by default — completion is how users avoid memorizing in the
first place. Unknown commands should suggest near-matches ("did you mean `categorize`?") rather than
dumping full usage.

Not all users are human. Agents drive these tools too, and self-describing commands matter *more* for
them: an agent knows `awk` and `grep` from training data, but carries no such knowledge of your tool —
every output it produces (help, results, errors) is the only interface description the agent has. A
surface that fully explains itself needs no separate agent documentation; one that doesn't gets driven
by guesswork.

## 8. Errors teach the next step

An error answers three questions: what happened, why, and what to do now — ideally with the exact
command to run. "Error: --branch requires --dir" is good; better appends "try: `hopper add '…' --dir
~/proj --branch main`". An error that only restates the failure sends the user back to the docs, which
is the failure mode these principles exist to prevent.

## 9. Feedback proportional to duration and consequence

Fast operations succeed quietly with a one-line confirmation. Long operations show progress — or queue
as async jobs with a way to watch (e.g. `--inline` to stream vs. default-queued). Nothing should sit
silent for ten seconds; nothing trivial should print a screenful.

## 10. Leave the machine as you found it

Installation is one obvious action (single binary, `uv tool install`, or brew); uninstallation is
equally obvious and complete. Keep state and config in predictable, documented locations (XDG
conventions, or one clearly-named directory), never scattered. First run is a `setup` wizard that gets
the user to a working state, not a wall of "edit this config file first." A tool that removes cleanly is
a tool users will risk trying.

## 11. Split the client from the daemon

When a tool needs background state — schedules, queues, long-running jobs — split it: a stateless CLI
client and a separate daemon (`tool`/`toold`), talking over a local API. The CLI stays fast and simple;
secrets and state live in one process; and the boundary is itself a composable seam other clients can
speak to.

## 12. Ship a companion skill

Every tool should ship a companion agent skill — the runtime guidance that lets an agent drive it well
(see §7: agents arrive knowing nothing about your tool). Install the companion skill at **global scope
by default** (`<tool> init`) — a companion skill describes the tool, not the project — with `--local`
opting into project scope. Where shared skill-install infrastructure exists, install through it rather
than hand-rolling embed-copy-version-guard logic per tool; the tool's surface stays simple while the
machinery is written once.

## Reviewing a CLI against these principles

A CLI UX review walks the tool's *surface*, not its code:

1. Run `--help` at every level (top-level and each subcommand).
2. Run each read-only command and note its output shape.
3. Plan each mutating command (dry-run) — do not `--apply` during a review.
4. For each principle, note conformances and violations, citing the exact command or flag.

Order the findings by **user pain, not principle number** — a missing `--json` on the most-scripted
command outranks a naming nit on a rarely-used one. Use this structure:

```
## CLI UX Review: <tool>

### Findings (most user pain first)
1. [§N Principle] <what's wrong> — cite exact command/flag; state the fix.
2. ...

### Exemplary (keep doing)
- <what the tool already does well>, cited.
```

## Reference material

For illustrative fleet exemplars (a table of tools scored against these principles) and the prior-art
sources these principles align with, read `references/exemplars-and-prior-art.md`. Load it when the user
wants worked examples of the principles in real tools, or the external standards behind them — it is not
needed to apply or review against the principles above.
