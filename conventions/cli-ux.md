---
name: cli-ux
scope: "UX principles for command-line tools — grammar, flags, output, safety, discoverability, install footprint"
does-not-cover: "TUI/full-screen applications, daemon internals, language-specific CLI framework usage"
metadata:
  version: "0.1.0"
  author: Stacey Vetzal
---

# CLI UX Principles

Command-line tools ask users to carry the interface in their heads. Every inconsistency — a flag that means something different here than there, a verb that's `remove` in one tool and `delete` in another — is a tax on memory, and for people not yet comfortable at the command line, it's a source of fear. These principles exist so that our tools feel like one coherent system: learn one, and you've mostly learned them all.

Two commitments frame everything below:

- **The Unix philosophy, at a humane altitude.** Small composable programs, but composition doesn't require every program to be low-level. A domain of related commands grouped under one easy-to-install executable (`gilt`, `parite`, `foundry`) is still a small program from the shell's point of view — it pipes, it exits, it composes.
- **The user's memory is the scarcest resource.** Optimize for predictability over cleverness. A user who can *guess* the right command without reading docs is the success condition.

## 1. Consistency beats cleverness

A fleet of tools should feel like one author wrote them. Before inventing a new verb, flag, or output shape, check whether an existing tool in the fleet already has a convention for it — and follow it, even if you can imagine something marginally better. Divergence needs a reason; convergence doesn't.

## 2. One domain, one executable

Group a domain's commands under a single binary with subcommands rather than scattering `tool-this`, `tool-that` executables across the PATH. One name to remember, one thing to install, one thing to uninstall. Keep the hierarchy shallow: `tool verb` for small tools, `tool noun verb` for larger domains. Three levels deep is a smell — it means the domain wants to be split or the grammar is fighting you.

## 3. A small, shared verb vocabulary

Use imperative base-form verbs, and reuse the same ones everywhere: `add`, `list`, `show`, `edit`, `remove`, `run`, `status`, `search`, `init`, `setup`. Never offer synonyms for the same idea (`update` vs `promote` vs `sync` in one tool forces the user to learn three fine distinctions), and never use the same verb for different ideas in two tools. Kebab-case for compound names (`check-quality`, `mark-duplicate`), never underscores.

## 4. Flags are a shared vocabulary too

The same flag means the same thing in every command and every tool:

- `--json` — machine-readable output (see §6)
- `--dry-run` / `--apply` or `--write` — mutation gating (see §5)
- `--yes` — skip confirmation prompts (scriptability escape hatch)
- `--force` — override a safety refusal, never a synonym for `--yes`
- `--quiet` / `--verbose` — volume control
- Kebab-case always (`--dry-run`, never `dry_run` — including in flag *values*)

In code, define flags once in a canonical options module and reuse them across commands (evt's `cli_options.py` is the reference pattern) — consistency enforced by construction, not by review.

## 5. Safe by default: plan, then apply

Commands that mutate state show what *would* happen by default and require an explicit flag to do it. Pick one gate per tool and use it uniformly: `--write` (gilt) or `--apply` (parite) — both are fine; mixing them in one tool is not. Corollaries:

- Mark mutating commands in their help text (`[Mutates]` / `[Mutates with --apply]`, parite's convention) so the read/write boundary is visible before running anything.
- Read-only commands must NOT carry a `--dry-run` flag — a safety flag on a safe command teaches users the flag is meaningless.
- Confirmation prompts always have a `--yes` bypass; a prompt with no bypass makes the tool unusable in scripts.
- After a mutation, report what changed in countable terms ("categorized 14 transactions, 2 skipped").

## 6. Human output on the terminal, machine output on demand

Default output is for humans: tables, color, relative times. But every command that reports data also accepts `--json` — a tool without machine output is a tool that can't be composed, scripted, or watched by an agent. Rules:

- Data goes to stdout; progress, warnings, and chatter go to stderr — so pipes carry data, not noise.
- Streams (logs, event feeds) emit JSONL, one object per line, jq-friendly.
- Detect the terminal: no color and no interactive prompts when stdout isn't a TTY; respect `NO_COLOR`.
- Exit codes are API: `0` success, nonzero distinguishes failure classes where callers care (cmx's `doctor` exiting `2` for "actionable issues found" is the pattern).

## 7. Help is the front door

Most users meet a tool through `--help`, not the README. Every command's help carries a one-line summary and at least one realistic, copy-pasteable example. Top-level help reads as a scannable map of the domain. Shell completions ship enabled by default — completion is how users avoid memorizing in the first place; disabling it discards the cheapest discoverability we have. Unknown commands should suggest near-matches ("did you mean `categorize`?") rather than dumping full usage.

## 8. Errors teach the next step

An error message answers three questions: what happened, why, and what to do now — ideally with the exact command to run. "Error: --branch requires --dir" is good; better is appending "try: `hopper add '…' --dir ~/proj --branch main`". An error that only restates the failure forces the user back to the docs, which is the failure mode we exist to prevent.

## 9. Feedback proportional to duration and consequence

Fast operations succeed quietly with a one-line confirmation. Long operations show progress — or queue as async jobs with a way to watch (`--inline` to stream vs. default-queued, parite's pattern). Nothing should sit silent for ten seconds; nothing trivial should print a screenful.

## 10. Leave the machine as you found it

Installation is one obvious action (single binary, `uv tool install`, or brew); uninstallation is equally obvious and complete. Tools keep state and config in predictable, documented locations (XDG conventions, or one clearly-named directory), never scattered. First-run experience is a `setup` wizard that gets the user to a working state, not a wall of "edit this config file first." A tool the user can remove cleanly is a tool they'll be willing to try.

## 11. Split the client from the daemon

When a tool needs background state — schedules, queues, long-running jobs — split it: a stateless CLI client and a separate daemon (`parite`/`parited`, `foundry`/`foundryd`), talking over a local API. The CLI stays fast and simple; secrets and state live in one process; and the boundary between them is itself a composable seam (other clients can speak the same API).

## Reviewing a tool against these principles

A CLI UX review walks the tool's surface, not its code: run `--help` at every level, run each read command, plan each mutation. For each principle above, note conformances and violations with the exact command/flag cited. The output is a findings list ordered by user pain, not by principle number — a missing `--json` on the most-scripted command outranks a naming inconsistency on a rarely-used one.

## Where our fleet stands (2026-07 baseline)

Observed in review of foundry, hopper, gilt, evt, parite, and context-mixer — kept here as the motivating evidence and the seed of each tool's improvement backlog:

| Tool | Exemplary | Gaps |
| ---- | --------- | ---- |
| gilt | dry-run default with `--write` gate; shared option helpers | no `--json` anywhere; shell completions explicitly disabled |
| evt | canonical `cli_options.py`; pervasive `--json`; JSONL streaming | mixed command grammar; `--dry-run` present on read-only commands |
| foundry | grouped `registry`/`sentinel` subcommands; span-tree traces | `--throttle dry_run` (underscore value); no `--json` on core commands |
| hopper | `--json` on all commands; examples in help; single-binary distribution | hand-rolled arg parser; mixed verb styles (`requeue` vs `cancel`) |
| parite | plan/apply split; `[Mutates]` help annotations; `setup` wizard; clean client/daemon split | `--json` only on `queue log`; third-level nesting under `memory` |
| context-mixer | `doctor` with semantic exit code 2; dry-run support | `update`/`promote`/`sync` synonym overload; no `--json`; prompts without `--yes` |

## Prior art

This field is well-trodden; these principles deliberately align with it rather than reinvent:

- [Command Line Interface Guidelines](https://clig.dev) — the closest thing to a community consensus document
- [12 Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46) (Jeff Dickey, Heroku)
- POSIX Utility Conventions & GNU `--long-option` standards
- `NO_COLOR` (no-color.org) and XDG Base Directory conventions
