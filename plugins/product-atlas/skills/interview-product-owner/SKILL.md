---
name: interview-product-owner
description: >
  Ask unresolved Product Atlas questions, curate the answers into intent topics,
  and delete answered question files. Use for product-owner interviews grounded
  in existing code or documentation, with the goal of no unresolved questions.
metadata:
  version: "2.0.1"
  author: Stacey Vetzal
---

# Interview the product owner

Read [the workspace rules](../../references/workspace.md) and
[the intent and question rules](../../references/registries.md).

Apply the source check. Read questions and their evidence. Check the related
intent before asking, so the owner does not have to repeat a settled decision.
Prioritize unclear purpose and differences that affect users. Respect the requested
scope and deferred questions' revisit conditions.

Ask one question at a time by default. Explain the current behavior and why the
answer matters. Offer options only when they represent real alternatives.
Allow another answer and "I don't know". Avoid leading questions and code jargon.

When confirmed intent conflicts with code or documentation, explain the difference
through its effect on users. Ask whether to bring the behavior and documentation
into line with that intent, plus any product questions needed to proceed.
Do not ask the owner to choose code structures or weaken intent to fit current code.
If intent already records the request to change behavior, skip that decision.
Ask only about product choices that remain unclear. Implementation can be behind
clear intent without making the owner's direction uncertain.

After each answer, curate the relevant intent topic. Save the attribution and
change history, repair active references, and delete the answered question.
Do not collect answers in question files or create a separate intent file for each.
Ask a narrow follow-up when the answer is incomplete. Never interpret silence as
agreement.

Reconcile each answer with the affected code and source documentation. A policy
answer may leave a different question about alignment or evidence. Keep that
remaining question focused. Do not ask the settled policy question again.

Intent remains after questions close. Keep topic sections succinct, combine
duplicate statements, and preserve the purpose, conditions, and attribution.

Keep deferred and partly answered questions in the folder. If evidence is needed
instead of another owner answer, say what would resolve the question. Do not keep
interviewing the owner for facts that require inspecting implementation.

End with the topics updated and questions remaining. An empty folder is the goal,
but report alignment only after a current review of the stated scope. If generated
documentation is stale, say it needs regeneration. Use the generation command's
rules when the user also asks to regenerate it.
