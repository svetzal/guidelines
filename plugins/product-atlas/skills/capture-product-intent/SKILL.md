---
name: capture-product-intent
description: >
  Curate product-owner answers and decisions into topic-based Product Atlas
  intent files, then delete answered questions. Use when the user clarifies
  product behavior in a repository with existing code or documentation.
metadata:
  version: "2.0.0"
  author: Stacey Vetzal
---

# Capture product intent

Read [the workspace rules](../../references/workspace.md) and
[the intent and question rules](../../references/registries.md).

1. Apply the source check and identify the affected topic and scope.
2. Read related intent, unresolved questions, and relevant history.
3. Curate the answer into the topic, with its conditions and attribution.
4. Combine related statements into readable sections and remove repetition.
5. Save the change history and repair active references.
6. Delete questions that the answer resolves, after checking the saved intent.
7. Reconcile the affected intent with current code and source documentation.
8. Report remaining questions and whether documentation needs regeneration.

Do not create one intent file per answer. Group related expressions of intent
under topic headings. Preserve meaning when combining, moving, or splitting sections.
Keep earlier wording in history. Capture spontaneous intent without inventing a
question to justify it.

A partial answer leaves a narrower question. A settled policy with contradicting
code needs a distinct alignment question, not another copy of the policy question.
Never delete unresolved differences merely to empty the folder.

Do not edit source files or generated documentation here. Save corrections in
intent and regenerate the documentation only when the user requests it.
