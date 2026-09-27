---
name: product-experience-design
description: >-
  Reimagine, audit, or implement Bedrock and Roost product UIs using their actual
  Epilogue Tracker intent, domain meaning, and reusable controls and compositions
  from the Bedrock customer catalogue. Use for UI redesigns, workflow reviews,
  design-system adoption, and component or workspace changes in these two
  products. Preserve each product's visual identity and operational boundaries.
metadata:
  version: "1.0.2"
  author: Stacey Vetzal
---

# Product experience design

Apply one design theory to distinct products. Bedrock and Roost keep their own
colours, typography, layout conventions and responsibilities. Borrow reusable
presentation from the customer catalogue; do not turn either management product
into a customer application or force both into the same shell.

## Locate the work

Read the current repository's AGENTS.md and charter. Identify the target product
from source ownership, not from a nearby checkout or the appearance of a screen.
Load [product contexts](references/product-contexts.md) for source locations,
audiences and critical distinctions. Read only the relevant product section.

Use this skill within the user's requested scope. An audit produces findings and
a concrete proposal; an implementation request produces a working increment.
Installing or invoking this skill does not authorize a wholesale redesign,
tracker mutation, deployment, or new operational authority.

## Start with the actual product model

Run `et` from the target product root where its own `.et_env` lives. Never print,
copy or reuse the token from another product. Read the current model rather than
assuming that example IDs remain current:

```sh
et charter --json
et list actors --all --json
et list goals --all --json
et list interactions --all --json
et list journeys --all --json
et validate --json
```

Include all states during discovery: default listings can omit already-created
work. Distinguish current intent and implemented entries from deleted or discarded
history; do not infer a missing actor from the default list. For large models,
use the installed CLI's documented filters after identifying
the relevant Actors and Goals. Reconcile the charter with source evidence; a
model entry is not proof that a feature is installed or available to that actor.
Check local help before constructing create/update commands. The live CLI may
represent relationships differently from Bedrock's portable customer-model JSON.

Name the Actor, Goal and Interaction served by the change. A Journey names its
beneficiary; each Interaction names its performer. Operators may support a
customer's Goal without giving customers the operator's permissions.

If the correct actor or Journey is missing, state the gap and draft the missing
intent in business terms. Make useful source and visual analysis while the gap is
resolved. Update the actual tracker when the user has authorized product-model
work; do not fabricate existing IDs or mark work complete from a mockup. If tracker
access is unavailable, preserve the uncertainty and use verified local evidence.

## Trace meaning into the interface

Use [model and composition contracts](references/design-contracts.md) to describe:

- Ordered Journey stages, performers, context and handoffs.
- Domain identities, value objects, references, derived facts and lifecycle rules.
- Projections that collect the information needed for each task.
- Commands with inputs, authority, preconditions, effects and recovery.
- Bindings that separate read-only facts, view-state changes and business changes.
- Compositions and their component dependencies, including states and accessibility.

These form a graph of meaning, not a single screen hierarchy. Reuse stable IDs
across views. Keep selected identity separate from its label. Never infer edit
permission from a field type, or domain semantics from a database column name.

Use the owner's or operator's language in the UI. Keep technical detail where it
supports a real decision: a Roost operator may need a source SHA, dependency or
observation time. A Bedrock business owner usually needs the outcome and next step.
“Request electrical service” avoids the employment ambiguity of “Ask about a job.”
Name what an action actually does; saving a status is not sending a message.

## Reuse the library deliberately

Before inventing a control or pattern, follow
[borrowing the catalogue](references/component-reuse.md). Inspect its implementation,
interaction contract, examples and tests. Reuse semantics and suitable presentation
code under the receiving product's ownership. Map visual roles to that product's
existing tokens. Do not introduce a runtime dependency on Shop, Bedrock or Roost
internals merely to obtain a button, table or inspector.

Prefer a small vocabulary of shared controls and patterns over page-specific
variants. A select, input and adjacent button should align in height and baseline.
Standardize states, keyboard operation, focus and validation as well as appearance.

## Reimagine by Journey, implement in coherent increments

Inspect representative screens with browser control when available. Capture the
current work, navigation and layout before editing. Choose one useful Journey and
map its information needs before deciding which parts of the existing layout fit.
Preserving a product's identity does not require preserving an ineffective layout.

Keep frequent controls compact and related facts visible together. Use tables for
comparison, inspectors for selected context, forms for command inputs, agendas for
time order and history for evidence. Avoid repeated business identity, excessive
nested panels and empty space that separates information needed for one decision.

Show intended compositions at each Journey stage. Inline examples and shared
selection make handoffs reviewable; a set of links to disconnected screenshots
is insufficient. In the actual product, retain sensible routes and workspaces:
a Journey demonstration does not require one enormous production page.

Classify each proposed change:

- **Presentation:** tokens, hierarchy, density, component use or arrangement.
- **Interaction:** navigation, selection, draft retention, feedback or task order.
- **Business behaviour:** policy, permissions, lifecycle, command effects or data.

Prefer presentation and interaction changes that preserve business contracts.
If a coherent workflow needs behaviour changes, describe the business reason,
affected model relationships, data and authority implications, and acceptance
examples. Include justified changes within the user's authorization; clarify only
material unresolved business decisions. Do not conceal a behaviour change as
styling or block an authorized functional improvement merely because this is UI
work.

## Verify and leave evidence

Check the complete Journey with representative synthetic records and meaningful
invalid, empty, stale, denied and recovery states. Preserve source facts when
editing derived views. Reuse real pure validation in demonstrations without
triggering live persistence, messages, deployments or recovery operations.

For tables, verify sortable headings, bounded data, compact search, selection and
usable row targets. Keep native keyboard actions available when rows are clickable.
Use photos where recognition benefits; missing photos must remain understandable.

Verify native semantics, accessible names and descriptions, unique IDs, logical
reading order, error association, visible focus and meaningful announcements.
Inspect narrow and wide layouts, zoom and supported themes. Render repeated
compositions with isolated state and IDs or show one selected trace at a time.
Target WCAG 2.2 AA; automated tests do not establish conformance.

Run the repository's applicable checks. Record the source revision and component
provenance, affected et entities, before/after evidence, behavioural changes and
remaining limits. Keep proposed, demonstrated, implemented, verified and deployed
claims separate. Show where the user can find the result. Preserve customer and
product boundaries through the normal release process.
