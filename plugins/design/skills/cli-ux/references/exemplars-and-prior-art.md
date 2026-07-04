# CLI UX — Exemplars and Prior Art

Read this when the user wants worked examples of the principles in real tools, or the external standards
they align with. Not needed to apply or review against the principles in `SKILL.md`.

## Fleet exemplars (2026-07 baseline)

Observed in review of a fleet of small tools — kept as motivating evidence and the seed of each tool's
improvement backlog. The pattern to notice: even strong tools carry gaps, and the gaps cluster around
the same principles (missing `--json`, non-standard mutation gates, synonym-overloaded verbs).

| Tool           | Exemplary                                                                 | Gaps                                                                                     |
| -------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| gilt           | dry-run default on all mutations; shared option helpers                   | gate is `--write` rather than the standard `--apply`; no `--json` anywhere; completions off |
| evt            | canonical `cli_options.py`; pervasive `--json`; JSONL streaming           | mixed command grammar; `--dry-run` present on read-only commands                          |
| foundry        | grouped `registry`/`sentinel` subcommands; span-tree traces               | `--throttle dry_run` (underscore value); no `--json` on core commands                     |
| hopper         | `--json` on all commands; examples in help; single-binary distribution    | hand-rolled arg parser; mixed verb styles (`requeue` vs `cancel`)                         |
| parite         | plan/apply split; `[Mutates]` help annotations; `setup` wizard; clean client/daemon split | `--json` only on `queue log`; third-level nesting under `memory`               |
| context-mixer  | `doctor` with semantic exit code 2; dry-run support                       | `update`/`promote`/`sync` synonym overload; no `--json`; prompts without `--yes`          |

How to read the table in a review: the "Exemplary" column shows the convention already met (cite it as
a "keep doing"); the "Gaps" column shows the exact violation and which principle it maps to.

## Prior art

This field is well-trodden; these principles deliberately align with it rather than reinvent:

- [Command Line Interface Guidelines](https://clig.dev) — the closest thing to a community consensus document
- [12 Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46) (Jeff Dickey, Heroku)
- POSIX Utility Conventions & GNU `--long-option` standards
- [`NO_COLOR`](https://no-color.org) and the XDG Base Directory conventions
