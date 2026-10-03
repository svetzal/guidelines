---
name: reconcile-product-evidence
description: >
  Compare Product Atlas intent topics with code and source documentation.
  Maintain questions for unclear purpose or differences, and delete questions
  when evidence resolves them. Use after source changes or to check alignment.
metadata:
  version: "2.0.0"
  author: Stacey Vetzal
---

# Reconcile product evidence

Read [the workspace rules](../../references/workspace.md) and
[the intent and question rules](../../references/registries.md).

Apply the source check. Read current sources and related intent topics. Consult
history for earlier evidence, but do not treat it as proof of current behavior.
Missing source material is an evidence gap, not proof that a feature disappeared.

For each affected actor, goal, interaction, or journey:

1. Identify the intent and its source or owner attribution.
2. Compare it with current code and source documentation.
3. Create or refine a question for each unresolved difference or unclear purpose.
4. Search intent and history before asking a previously settled question.
5. Curate new understanding into the appropriate intent topic.
6. Save evidence and resolution history, then delete resolved question files.

When intent is clear but code differs, keep one alignment question for that gap.
A promised fix is not evidence of alignment. When code changes resolve it, update
the intent topic's evidence and remove the question. Do not silently change desired
behavior to match the implementation.

Refactor intent topics when needed. Group related statements, remove repetition,
and update references when sections move. Keep confirmed intent distinct from
inference and disputed claims.

Write a dated review under the configured `history/` directory. Include source
revisions, reviewed scope, intent references, remaining questions, and conclusions.
Every known gap must have an unresolved question. Missing or stale evidence must
not produce an empty folder and a false claim of alignment.

Report no open questions only after checking the current sources and scope.
The next generation updates the stakeholder documentation. Do not patch generated
pages, modify implementation, or dispatch coding work during reconciliation.
