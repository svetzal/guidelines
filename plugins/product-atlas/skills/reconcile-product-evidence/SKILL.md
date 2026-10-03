---
name: reconcile-product-evidence
description: >
  Compare Product Atlas intent with code and documentation, maintain unresolved
  questions without duplicates, and identify implementation drift. Use when
  sources change or the user asks whether the system matches product intent.
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---

# Reconcile product evidence

Read [the workspace contract](../../references/workspace.md) and
[the registry contract](../../references/registries.md).

Apply the source gate. Read affected source material and related intent. Consult
generation records for previous revisions, but inspect current files before
asserting current behavior. A missing source is unavailable evidence, not proof
that a feature disappeared.

For each affected actor, goal, interaction, or journey:

1. Describe the implementation evidence and its limits.
2. Identify confirmed intent and distinguish inferred intent.
3. Record agreement, contradiction, or an evidence gap with source references.
4. Reuse an existing question for the same underlying decision.
5. Create a question when a new conflict needs product clarification.
6. Preserve answered questions when the mismatch is already understood.

Update wording and evidence as understanding improves. Preserve IDs, answers,
and revision history. Do not promote code-derived intent to confirmed status.
Do not change recorded intent merely to match the implementation.

Write a dated reconciliation record under the configured generation directory.
Include scope, inspected revisions, intent IDs, question IDs, and unresolved drift.
Report partial coverage explicitly. Do not claim the whole product was checked
after inspecting only one area.

The generated drift report changes on the next wiki generation. Do not patch
it here, change implementation, or dispatch coding work as part of reconciliation.
