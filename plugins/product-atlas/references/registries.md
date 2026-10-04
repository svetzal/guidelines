# Intent and questions

`intent/` explains what the product should do. `questions/` contains only
unresolved questions. Move answers into intent, then delete the question files.
Keep the record of changes in `history/`, outside both folders.

Intent is a lasting statement of purpose. Keep it after the implementation and
documentation align. It continues to guide later changes. Remove or replace its
meaning only when the product owner explicitly changes that purpose.

Confirmed intent sets the direction for code and documentation. When they differ,
identify the changes needed to follow that intent. Ask the owner any remaining
product questions in plain language. Do not weaken intent to match existing code.
Keep inferred or disputed intent clearly marked until the uncertainty is resolved.

Intent can describe future behavior before code implements it. Preserve that
direction and show what still needs to change. A planned gap is different from
an unexplained conflict. Do not infer that intent is wrong because code is behind.
Once the owner has requested the direction, do not ask whether they still want
it on every review. Keep any remaining question focused on an unresolved product
choice or the evidence needed to show alignment.

The goal is an empty `questions/` folder after a current review. That means the
reviewed implementation, source documentation, and intent agree, with no known
uncertainty about their purpose. Never hide a known gap to reach that state.

## Curate intent by topic

Use readable topic filenames, such as `order-cancellation.md` or `account-access.md`.
Group related expressions of intent into sections within each file. Do not
create one file per answer, question, or individual statement.

Each topic file has YAML frontmatter with `topic_id`, `title`, and `updated_at`.
Use a UUID-based topic ID. In each section, explain:

- What the product should do and who benefits.
- Why it matters, when known.
- The conditions and exceptions.
- Whether the intent is confirmed, inferred, or disputed.
- Who confirmed it and when, or which sources support the inference.

For example, `order-cancellation.md` could contain sections for the cancellation
cutoff, refunds, and exceptions. A later answer about refunds belongs in that
file. Rewrite the relevant section into a coherent statement instead of appending
a transcript or a separate answer record.

Reference intent with a path and heading, such as
`order-cancellation.md#cancellation-cutoff`. Paths are relative to `intent/`.
When you move or rename a section, update active references. Record the old and
new locations in history. Generated documentation picks up those changes on
its next run.

Regularly combine overlapping statements, remove repetition, and split topics
that have become unrelated. Preserve meaning, conditions, evidence, and attribution.
Keep each expression of intent succinct. Merge duplicate files or sections while
retaining their meaning and repairing references. Put detailed discussions and
change narratives in history, with short evidence references in the topic file.
Keep superseded wording in history, not as conflicting current guidance in intent.
Do not invent rationale or turn a qualified answer into an unconditional promise.

An explicit product-owner answer can confirm intent without another approval.
If authority or meaning is unclear, record that uncertainty and keep a focused
question. Code can support an inference, but cannot by itself confirm desired policy.
An approved source document can establish intent when its authority is clear.

## Keep only unresolved questions

Store one unresolved question per Markdown file, named `Q-<uuid>.md`.
The filename identifies the question while it is open. Clarifying its wording
keeps the same ID. Do not leave README files, placeholders, answered records,
or superseded records in `questions/`. It must be possible for the folder to be
empty.
Create the folder after the source check if it is absent. Do not add a placeholder
just to make Git retain an empty directory.

Each question has YAML frontmatter with:

| Field | Meaning |
| --- | --- |
| `id`, `title` | Stable ID and the question in plain language |
| `decision_key` | Semantic key for the decision or gap |
| `kind` | `purpose`, `alignment`, or `evidence` |
| `status` | `open` or `deferred` only |
| `intent_refs` | Related topic sections, or an empty list |
| `entities`, `scope` | Affected users, behavior, and conditions |
| `sources` | Evidence for the question |
| `answerable_by` | The person or evidence that can answer it |
| `priority` | `high`, `medium`, or `low` |
| `created_at`, `updated_at` | ISO dates |

The body explains why the question matters and what would resolve it. For a
known implementation gap, state what evidence of correction is needed. A deferred
question stays in the folder, with its reason and revisit condition.

Write titles and owner-facing explanations in product language. Explain who is
affected and what they can or cannot do. Keep code paths and technical evidence
in a separate evidence section. Ask about changing product behavior and its
documentation, not about functions, database fields, or other implementation details.

Before creating a question, search current questions, related intent, and relevant
history. Match the underlying decision, user, and scope, not only its wording.
Reuse a current question for the same unresolved issue. If intent already answers
the policy question, do not ask it again. New evidence can justify a new question,
but explain what changed.

When combining duplicate questions, preserve their evidence in the surviving
question. Record the merge in history and delete the duplicate. Do not replace
one unresolved question with several rewordings of it.

## Turn an answer into intent

1. Read the current question and related intent topics.
2. Curate the answer into the appropriate topic sections.
3. Preserve attribution, conditions, and the evidence used.
4. Record the answer and changed intent locations in `history/changes/`.
5. Check that the saved intent covers the answer before deleting anything.
6. Replace active references to the answered question with intent or history references.
7. Delete the answered question file.
8. Reconcile the affected intent with current code and source documentation.

Do not delete a partly answered question. Narrow it to the remaining uncertainty.
Never interpret silence as agreement. If writing intent or history fails, retain
the question. Before deletion, check for concurrent edits to the question.

History records use dated UUID filenames. Record the question ID, its wording,
the answer, attribution, changed intent sections, and evidence of any resolution.
Use available conversation references without inventing transcript links. History
preserves the explanation of changes. It is not another queue of questions.

## Resolve differences without losing settled intent

Answering a policy question does not make contradicting code correct. Delete the
answered policy question after saving the intent. Keep or create one distinct
alignment question for the remaining difference. Link it to the settled intent.
Do not reopen the policy question merely because the same code remains unchanged.

For example, an owner confirms that paid orders can be cancelled before dispatch.
Curate that answer into `order-cancellation.md` and delete its policy question.
If code still rejects paid cancellations, ask: "Should we update cancellations
and the customer guide so buyers can cancel until dispatch?" Explain that this
would bring them into line with the recorded intent. Once the owner requests
that change, do not ask the same question again. A plan does not prove completion.
Skip that question if the intent already records the request to make this change.
Once that plan is recorded, narrow the question to the missing evidence of alignment.
Do not keep asking for a policy decision that the owner already supplied.

When current evidence answers the remaining alignment question, update the topic's
evidence, record the resolution, and delete the question. Repeated reviews reuse
the same unresolved question until then. These skills do not authorize source edits.
Keep the intent topic after resolution. Update its evidence and remove duplicate
wording as needed, but do not delete the purpose because the code now meets it.

Create evidence questions for missing source material, unreviewed relevant areas,
and unclear purpose. A documentation-only review can run, but cannot establish
implementation alignment without implementation evidence. Keep that limitation
as a question, not only a footnote in generated output.

After reconciliation, an empty folder means no known unresolved questions in the
reviewed scope. Report that scope and the inspected revisions in history and the
generated documentation. Do not claim alignment from an empty folder before review,
after manual deletion, or when sources have changed since the last review.
