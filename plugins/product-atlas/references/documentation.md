# Documentation generation contract

Use this contract only for the generation command. The workspace and registry
contracts also apply. The documentation is a complete generated view of curated
intent
and inspected sources. It is never the authoritative store for intent or answers.

## Digest the corpus

Run preflight before creating output. Read useful code or documentation and
state the available coverage. Stop if there is no product material to digest.
An empty directory, generic scaffold, or unrelated README is not a corpus.

With documentation alone, describe documented behavior. State that the current
implementation is unverified. With code alone, distinguish code evidence from
runtime observation. Do not invent application behavior, analytics, or user feedback.

Read relevant code in place, including tests and configuration. Use these signals
as starting points, not automatic conclusions:

| Signal | Possible product meaning |
| --- | --- |
| Routes, controllers, endpoints | Actions and interactions |
| Role and permission models | Actor distinctions to investigate |
| Workflow engines and state machines | Journeys and transition rules |
| Validations and business rules | Conditions on interactions |
| Errors and recovery paths | Failure states and recovery interactions |
| Schema and migrations | Domain vocabulary and relationships |
| Tests | Expected behavior, edge cases, and domain language |

If authorized runtime access is available, inspect navigation and full workflows.
Record empty states, calls to action, and what each actor can see and do. Do not
perform transactions or change live data merely to complete the documentation.

Compare supplementary evidence with code and documentation. Record customer
terms alongside code terms when they differ. Explain the difference in ordinary
language. Internal team roles are actors only if the product serves those people.

## Preserve durable understanding

Read intent topics and unresolved questions before extraction. Curate new
inferences into related topic sections, with source evidence. Do not present
them as owner decisions. Apply the question matching rules before creating questions.

Record conflicts without rewriting intent to match code. Every unresolved
difference or unclear purpose needs a question. If policy is settled, link its
intent section and keep one alignment question for the remaining difference.
When evidence resolves a question, curate the intent, save history, and delete
the question file. Never preserve answered question files in the queue.

Keep `history/entities.json` outside the documentation. It maps stable entity
IDs to
type, slug, aliases, related IDs, evidence, status, last verification, and any
deprecation reason. It preserves identity across renamed pages and records
removals that a later generation must explain. It records earlier extraction results.
Current product intent belongs in the topic files. Never use it alone as
evidence of current behavior.

Keep dated run records in `history/runs/`. Record inspected source revisions,
uncommitted content where relevant, document hashes, coverage, and validation.
Use a run UUID in filenames. Do not overwrite records from earlier runs.

For subsequent runs, compare stored source revisions with the current corpus.
Use Git revision ranges and changed paths when available. Check uncommitted and
untracked source changes too. If revision ancestry is unavailable, inspect the
affected corpus again. A previous generation date alone is not enough.

Reusing unchanged evidence can reduce reading. Changes to shared rules, actor
models, or relationships require checking affected entities beyond changed files.
Regardless of incremental analysis, regenerate the complete documentation each time.

Missing sources make affected claims stale or unverified. Confirmed removal of
behavior deprecates its observed entity and records the supporting revision.
Retain deprecated pages and their explanation through the durable entity history.
An intended capability may remain valid after implementation removal. Show that
gap. Do not deprecate intent because a route or feature flag disappeared.

## Model the product

Use the Screenplay Pattern:

- An actor is a distinct user role defined by perspective and intent.
- A goal is an outcome that actor wants, expressed in the actor's language.
- An interaction is a discrete action that supports a goal.
- A journey is an ordered sequence from need to goal completion.

Use role-based actor slugs, outcome-based goal slugs, action-based interaction
slugs, and flow-based journey slugs. Preserve stable IDs independently of slugs.
Do not invent entities without source evidence or recorded, attributed intent.

Goals describe human outcomes, such as "recover access to my account".
Technology choices such as "implement OAuth" are not user goals.

Each entity has YAML frontmatter with:

- `id`, `type`, and `title`.
- `confidence`: `high`, `medium`, `low`, or `inferred` for the supporting analysis.
- `sources`: source IDs, paths, locators, and inspected revisions or dates.
- `intent_refs` pointing to topic sections and `question_ids` for unresolved questions.
- `last_verified`: actual verification date, or null if never verified.
- `status`: `active`, `stale`, or `deprecated`.
- `alignment`: `aligned`, `divergent`, `unknown`, or `not-assessed`.

Never advance `last_verified` simply because a page was rendered again. Explain
confidence and limitations in the prose. High confidence in code evidence does
not mean high confidence about user intent or deployed behavior.

## Render for stakeholders

Generate this structure:

```text
documentation/
  AGENTS.md
  index.md
  actors/
  goals/
  interactions/
  journeys/
  drift-report.md
  open-questions.md
```

Every page starts with a short generated-content notice. It directs corrections
to the configured registries and names the regeneration command. Generate an
`AGENTS.md` that prohibits direct page edits and states these same boundaries.
The notice and guidance are part of the generated output on every run.

The index explains the system, who it serves, source coverage, and verification
limits. It links to all actors and their goals, the drift report, unanswered
questions, and a separate list of deprecated entities.

Each entity page explains:

1. The human purpose and relevant product vocabulary.
2. Implemented or documented behavior, with its evidence and limitations.
3. Confirmed intent and separately labelled inferred intent.
4. Alignment or divergence, including scope and practical impact.
5. Related entities, evidence references, and unresolved questions.

Use "unknown" when the evidence cannot establish alignment. Do not describe an
intended interaction as available merely because it appears in an owner answer.

Intent can lead implementation. Explain which intended behavior already exists
and what the product still needs to do. Distinguish requested future changes from
unexplained differences. Do not present planned behavior as currently available,
or question settled intent simply because implementation is behind.

Actors link to their goals. Goals link to their actor, interactions, and journeys.
Interactions link to performing actors, supported goals, and journeys. Journeys
link to their protagonist, goal, and each ordered step. Make these links reciprocal.

The drift report pairs each intended claim with the observed or documented
claim, its evidence, and a relevant question or recorded decision. Distinguish
unresolved intent from a known implementation gap. Include vocabulary differences.

The questions page shows only unresolved questions, including deferred ones.
Link settled decisions to intent sections. Show question IDs and enough context
to understand them. Link entity pages to anchors in this generated questions
page, not to question files that will disappear when answered.

The index states whether questions remain and what scope the agent reviewed.
An empty question folder can support an alignment conclusion only after a current
review of implementation, source documentation, and intent. Do not report full
alignment with missing implementation evidence or unreviewed relevant areas.

## Validate and replace

Create the complete documentation in a fresh staging directory beside the output
path.
Name it `.product-atlas-stage-<run-uuid>`. Name the temporary backup
`.product-atlas-backup-<run-uuid>` so neither becomes evidence on a later scan.
Never clear the current documentation at the start of a run. Check that the
staging path
is outside every registry and outside source discovery for this run.

Validate the staged output:

- Every local link and fragment resolves in the final layout.
- Every intent reference resolves to a topic section. Every current question and
  entity ID exists.
- Entity links are reciprocal. Journey steps are ordered and valid.
- Actors have goals, goals have interactions, and interactions belong to journeys,
  or the page explains the evidence gap and links to its unresolved question.
- Deprecated entities are not presented as active capabilities.
- Staleness reflects relevant source changes, not unrelated commits.
- Each substantive claim has evidence or a clearly attributed intent reference.
- No inferred intent appears as confirmed. No documented claim implies runtime proof.
- Required pages and generated notices exist, with no scaffold placeholders.

Review the index and representative journeys for readable stakeholder language.
Record the checks and remaining limitations in history. Every missing piece of
evidence or known difference also needs an unresolved question. Fix broken links
and corrupt records before publication. Never claim alignment only because the
question folder happens to be empty.

Before replacement, repeat path checks and compare input revisions with those
used for generation. Stop or refresh analysis if inputs changed. Resolve links
relative to the final documentation path, not its staging name. Link external registry
paths appropriately for the local Markdown reader. Never copy registries into output.

If the output directory already has content, confirm it is a previous Product
Atlas output from its generated notice and a completed run record. If ownership
is unknown, preserve it and request a different output path or an explicit migration.
Never delete an arbitrary existing documentation directory.

Replace only the configured documentation directory after validation. Use a same-filesystem
rename with a temporary backup and rollback on failure. Do not merge individual
pages, since that would retain obsolete output. Preserve any Git metadata: if
the output directory is itself a repository, stop and request a dedicated output
subdirectory.
Remove the temporary backup only after checking the installed output. A failed
run keeps the previous documentation available and records its failure outside
the documentation.

A question about stale generated documentation closes only when replacement
succeeds. During staging, prepare its resolution and the final question view.
Keep the actual question file until the new output passes validation and installs.
Then record the resolution in history and delete it. On failure, retain it.
If final record updates fail, report the incomplete run and preserve the question.

Mark the run completed only after replacement succeeds. Save the new entity
inventory as part of that completed generation. Failed staging must not advance
the last successful source revision. Registry updates made during analysis remain
durable even when rendering fails. Mark the documentation as needing
regeneration in the
run record when its inputs are newer than the last successful output.

Report the documentation entry point, reviewed scope, and number of remaining
questions. When the folder is empty, state which current sources agree and the
revisions checked. If questions remain, explain what evidence or decisions will
resolve them.
