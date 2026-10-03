# Wiki generation contract

Use this contract only for the generation command. The workspace and registry
contracts also apply. The wiki is a complete generated view of durable records
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
perform transactions or change live data merely to complete a wiki.

Compare supplementary evidence with code and documentation. Record customer
terms alongside code terms when they differ. Explain the difference in ordinary
language. Internal team roles are actors only if the product serves those people.

## Preserve durable understanding

Load intent and questions before extraction. Record new inferred intent with
source evidence. Do not present it as an owner decision. Reuse existing records
for the same meaning. Apply the question matching procedure before every creation.

Record explicit conflicts without rewriting intent to match code. Create a
clarification question for a new unresolved conflict. Link an existing answered
question when the decision is already settled and only implementation differs.

Keep `generation/entities.json` outside the wiki. It maps stable entity IDs to
type, slug, aliases, related IDs, evidence, status, last verification, and any
deprecation reason. It preserves identity across renamed pages and records
removals that a later generation must explain. It is derived extraction history,
not an alternative intent registry. Never use it alone as evidence of current behavior.

Keep dated run records in `generation/runs/`. Record inspected source revisions,
uncommitted content where relevant, document hashes, coverage, and validation.
Use a run UUID in filenames. Do not overwrite records from earlier runs.

For subsequent runs, compare stored source revisions with the current corpus.
Use Git revision ranges and changed paths when available. Check uncommitted and
untracked source changes too. If revision ancestry is unavailable, inspect the
affected corpus again. A previous generation date alone is not enough.

Reusing unchanged evidence can reduce reading. Changes to shared rules, actor
models, or relationships require checking affected entities beyond changed files.
Regardless of incremental analysis, produce a complete new wiki each time.

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
- `intent_ids` and `question_ids`.
- `last_verified`: actual verification date, or null if never verified.
- `status`: `active`, `stale`, or `deprecated`.
- `alignment`: `aligned`, `divergent`, `unknown`, or `not-assessed`.

Never advance `last_verified` simply because a page was rendered again. Explain
confidence and limitations in the prose. High confidence in code evidence does
not mean high confidence about user intent or deployed behavior.

## Render for stakeholders

Generate this structure:

```text
wiki/
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

Actors link to their goals. Goals link to their actor, interactions, and journeys.
Interactions link to performing actors, supported goals, and journeys. Journeys
link to their protagonist, goal, and each ordered step. Make these links reciprocal.

The drift report pairs each intended claim with the observed or documented
claim, its evidence, and a relevant question or recorded decision. Distinguish
unresolved intent from a known implementation gap. Include vocabulary differences.

The questions page is a generated view of the registry. Include open questions,
deferred questions with revisit conditions, and links to answered decisions that
explain continuing drift. Render enough context for stakeholders to understand
the question without reading raw registry metadata. Never store the only copy
of an answer here.

## Validate and replace

Create the complete wiki in a fresh staging directory beside the output path.
Name it `.product-atlas-stage-<run-uuid>`. Name the temporary backup
`.product-atlas-backup-<run-uuid>` so neither becomes evidence on a later scan.
Never clear the current wiki at the start of a run. Check that the staging path
is outside every registry and outside source discovery for this run.

Validate the staged output:

- Every local link and fragment resolves in the final layout.
- Every referenced intent, question, and entity ID exists.
- Entity links are reciprocal. Journey steps are ordered and valid.
- Actors have goals, goals have interactions, and interactions belong to journeys,
  or the page explains the evidence gap and links to its question.
- Deprecated entities are not presented as active capabilities.
- Staleness reflects relevant source changes, not unrelated commits.
- Each substantive claim has evidence or a clearly attributed intent reference.
- No inferred intent appears as confirmed. No documented claim implies runtime proof.
- Required pages and generated notices exist, with no scaffold placeholders.

Review the index and representative journeys for readable stakeholder language.
Record the checks and any remaining limitations in the run record. Missing
evidence may be a stated limitation. Broken links and corrupt records must be fixed.

Before replacement, repeat path checks and compare input revisions with those
used for generation. Stop or refresh analysis if inputs changed. Resolve links
relative to the final wiki path, not its staging name. Link external registry
paths appropriately for the local Markdown reader. Never copy registries into output.

If the output directory already has content, confirm it is a previous Product
Atlas output from its generated notice and a completed run record. If ownership
is unknown, preserve it and request a different output path or an explicit migration.
Never delete an arbitrary existing documentation directory.

Replace only the configured wiki directory after validation. Use a same-filesystem
rename with a temporary backup and rollback on failure. Do not merge individual
pages, since that would retain obsolete output. Preserve any Git metadata: if
the wiki is itself a repository, stop and request a dedicated output subdirectory.
Remove the temporary backup only after checking the installed output. A failed
run keeps the previous wiki available and records its failure outside the wiki.

Mark the run completed only after replacement succeeds. Save the new entity
inventory as part of that completed generation. Failed staging must not advance
the last successful source revision. Registry updates made during analysis remain
durable even when rendering fails. Mark the wiki as needing regeneration in the
run record when its inputs are newer than the last successful output.

Report the final entry point, coverage, meaningful drift, unanswered decisions,
and any remaining verification limits.
