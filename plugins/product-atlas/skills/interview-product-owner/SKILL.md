---
name: interview-product-owner
description: >
  Ask a product owner unresolved questions from a Product Atlas question registry
  and record their answers as intent. Use for clarification interviews grounded
  in an existing code or documentation corpus, not greenfield product discovery.
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---

# Interview the product owner

Read [the workspace contract](../../references/workspace.md) and
[the registry contract](../../references/registries.md).

Apply the source gate. Read open questions and their evidence. Check related
answers before selecting a question. Prioritize decisions that affect users,
block interpretation, or explain substantial divergence. Respect a requested
product area and deferred questions' revisit conditions.

Ask one question at a time by default. Give a short explanation of the observed
behavior, the recorded intent, and the uncertainty. Offer options only when they
represent real alternatives. Allow another answer and "I don't know".
Avoid leading questions and implementation jargon.

Record each answer immediately using the registry contract. Preserve its scope,
attribution, and uncertainty. Confirm intent when an explicit owner answer is
clear. Ask a narrow follow-up when it is not. Do not demand repeated approval
for an answer the owner has already given.

Leave unanswered parts open. Defer a question when the owner cannot answer it;
record who or what could resolve it. Never interpret silence as agreement.
If no useful unanswered questions remain, say so instead of inventing an interview.

At the end, summarize decisions recorded, questions remaining, and whether the
wiki needs regeneration. Do not regenerate or edit the wiki during the interview
unless the user also requested generation. Generation uses the command's contract.
