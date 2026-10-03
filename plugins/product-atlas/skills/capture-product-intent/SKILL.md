---
name: capture-product-intent
description: >
  Record product intent from owner answers, corrections, or product discussions
  in a configured Product Atlas with an existing code or documentation corpus.
  Use when the user clarifies desired behavior or asks to record a product decision.
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---

# Capture product intent

Read [the workspace contract](../../references/workspace.md) and
[the registry contract](../../references/registries.md) before writing records.
These references are bundled with the complete Product Atlas plugin.

1. Apply the source gate and identify the affected actor, goal, and scope.
2. Read matching intent and questions, including answered and superseded records.
3. Capture the user's statement, rationale, qualifications, and attribution.
4. Refine an existing intent or record an explicit replacement decision.
5. Link questions answered by that decision and update their answer history.
6. Leave partially answered questions open. State the missing part precisely.
7. Report the recorded meaning and whether wiki regeneration is needed.

Use ordinary product language. Do not force the owner to supply entity IDs.
Link entities when known. An empty entity list is allowed until extraction
establishes them. Retain the scope so later extraction can make those links.

An answer can resolve uncertainty while code still contradicts intent. Preserve
that distinction. Capture spontaneous intent even when no question prompted it.
Do not invent a question solely to justify a statement already supplied.

Never edit the wiki or implementation here. If the user asks to correct a wiki
page, record the correction at its source and report that regeneration is needed.
