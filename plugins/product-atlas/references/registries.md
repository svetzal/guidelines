# Registry contract

Registries contain Markdown records with YAML frontmatter. One record represents
one intent or one question. Its filename is its stable ID plus `.md`.
Use `INT-<uuid>` for intent and `Q-<uuid>` for questions. Display short titles
to people; IDs are for references. Preserve IDs when titles or wording change.

Dates use ISO 8601. Evidence identifies a configured source ID, relative file
path, locator, and inspected revision or date. Cite test names or line ranges
when useful. Keep code evidence distinct from observations of a running system.

## Intent records

Required fields:

| Field | Meaning |
| --- | --- |
| `id`, `title` | Stable identity and readable title |
| `status` | `inferred`, `confirmed`, `disputed`, or `superseded` |
| `entities` | Stable actor, goal, interaction, or journey IDs |
| `scope` | Conditions, user group, product area, and exceptions |
| `sources` | Evidence references. Never a generated wiki page |
| `question_ids` | Questions that elicited or challenge this intent |
| `created_at`, `updated_at` | Record dates |
| `confirmed_by`, `confirmed_at` | Attribution, or null when unconfirmed |
| `supersedes` | Previous intent IDs, or an empty list |

The body contains the statement, rationale, evidence, and a revision history.
Preserve the answer's conditions and uncertainty. Do not turn a wish into an
unconditional commitment or invent a rationale the owner did not give.

An explicit answer or correction from the product owner can confirm intent.
Capture it without requiring a redundant approval. Ask a follow-up when the
answer is ambiguous. Keep the raw answer or a faithful excerpt with attribution.
Use the conversation date and available reference. Never invent a transcript URL.
If identity or authority is unknown, record that and leave the statement inferred.

Code-derived hypotheses remain `inferred`, even when implementation evidence is
strong. Explicit approved requirements in documentation can support confirmed
intent only when their authority and scope are evident. Otherwise, record them
as documented claims. Confidence in implementation does not confer authority
over intent. Conflicting authoritative statements remain disputed until resolved.

Refine the same record for wording or supporting evidence. For a changed product
decision, create a new intent record, link `supersedes`, and retain the old one.
Mark the old intent superseded only when the replacement decision is explicit.
Deleted code does not revoke intent.

## Question records

Required fields:

| Field | Meaning |
| --- | --- |
| `id`, `title` | Stable identity and current question |
| `status` | `open`, `answered`, `deferred`, or `superseded` |
| `decision_key` | Stable semantic key for the underlying decision |
| `entities`, `scope` | Affected entities and conditions |
| `intent_ids`, `sources` | Related intent and current evidence |
| `priority` | `high`, `medium`, or `low` |
| `answerable_by` | Product owner or another named source of authority |
| `created_at`, `updated_at` | Record dates |
| `answer_intent_ids` | Intent produced by answers, or an empty list |
| `superseded_by` | Replacement question ID, or null |

The body explains the uncertainty, its impact, current evidence, the answer
history, and wording changes. A deferred record also states the reason and the
condition for revisiting it. Do not repeat a deferred question without new cause.

### Match before creating

1. Identify the actor, goal, decision, and scope behind the finding.
2. Search all question statuses and relevant intent records.
3. Compare meaning, aliases, and scope, not just titles or literal keys.
4. If the decision already exists, reuse its ID and add only new evidence.
5. Clarify its wording if needed, preserving its answer and revision history.
6. Create a new question only when a distinct unresolved decision remains.

For example, "Can buyers cancel after dispatch?" and "When does cancellation
close?" may concern the same decision. A separate policy for business accounts
may need a different scoped question. A changed slug must not create a duplicate.

A repeated code mismatch does not reopen an answered intent question. Keep the
known intent and report continuing drift. Reopen the same question only when new
evidence challenges its answer for the same scope. State why and preserve history.
If the decision itself changes, create a linked successor question. When merging
accidental duplicates, mark one superseded and retain its references and answers.

## Evidence and divergence

Compare two dimensions separately:

- Intent authority: attributed owner decisions and approved requirements, then
  clearly marked hypotheses from the corpus.
- Observed behavior: analytics, feedback, observed application behavior, code,
  documentation, and marketing, with relevance, freshness, and limitations stated.

Use the gist's evidence ordering as an interpretation aid, not an automatic vote.
Analytics can show usage, but cannot decide desired policy. A test can express
an expectation, but cannot prove that a deployed system behaves that way.

For a new conflict, record both claims and ask what must be clarified. Never
silently choose one or modify the implementation. If the owner has already
settled that exact decision, link the answered question and keep reporting drift.
No new question is needed until there is new uncertainty.

A question is answered when its decision is sufficiently clear and its intent
records are linked. Drift is resolved only when current evidence shows alignment,
or an explicit change to intent removes the disagreement.
