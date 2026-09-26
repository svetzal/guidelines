# Model and composition contracts

Use the contracts needed for the current task. A small label change does not
require a full redesign dossier. A Journey revamp needs the relationships that
explain what must remain true when the UI is recomposed.

## From intent to components

A compact trace can use these columns:

| Stage | Beneficiary / performer | Interaction and outcome | Domain / projection | Composition | Effect and handoff |
| --- | --- | --- | --- | --- | --- |
| Review a candidate | Owner / owner | Decide whether the change fits | Pinned intent, preview and check evidence | Preview with decision context | Selection only; adoption is a separate command |
| Investigate availability | Customer / operator | Understand what is affected | System identity, dependencies and dated observations | System table with inspector | Selecting a system does not operate it |

These are examples, not existing et declarations or proof of available features.
Resolve the actual product's model and code before adopting them.

For each composition, state purpose, inputs, primary work, supporting context,
actions, feedback, view state, outputs, variants, recovery and evidence. Preserve
identity, permissions, units, validation and command effects when its layout changes.

Domain primitives and visual primitives are independent. An entity remains an
entity whether rendered as a select option, row, inspector or full workspace.
A value object groups business meaning without necessarily requiring a nested
database object. References are not automatically owned children.

Projection context can enrich a choice without expanding its effect. A parts
selector may show available quantity but selects an item ID. A system selector
may show health, source and placement but does not redeploy the selected system.

Use calendar dates for days, zoned timestamps for instants, and explicit units
for durations. Distinguish occurrence, recording and observation times. Ranges
need ordering and endpoint semantics. Unknown, absent, zero and empty differ.

## Authority and evidence

A command declares actor authority, permitted inputs, current-state guards,
transactional effects, duplicate handling and recovery. Recheck these at the
business boundary. Hiding a button does not authorize an event or HTTP request.
A status badge must not imply completion beyond the evidence it represents.

For example, a saved follow-up is not a reply, a built image is not a deployed
release, and an old healthy observation is not proof of current availability.
Keep uncertainty and timestamps visible when they affect the decision.

## Increment record

Capture enough of this record to review a substantive change:

- Product, source revision and current et Actor / Goal / Interaction / Journey.
- Current pain and evidence from actual screens and representative tasks.
- Proposed arrangement, component dependencies and token mapping.
- Behaviour preserved, deliberate changes and unresolved business decisions.
- Binding effects and authority boundaries.
- Acceptance examples, accessibility checks and recorded results.
- Component provenance and any missing library capability.

Prefer repository documentation and tests that remain useful after the task.
Do not copy credentials, operational records or full tracker exports into fixtures.
