# Harness implementation notes

These notes describe how an agent harness could use the intent library as a
dynamic source of guidance. They are a design direction, not a description of
the current intent record schema.

The central constraint is that the agent's context is a deliberately managed
working set. Guidance should be selected, injected, refreshed, superseded, and
retracted as the engineering objective develops. A harness should not append
every potentially relevant intent and rely on automatic context compaction to
recover space later.

## Design principles

- Sensors establish what appears to be true about the current work.
- Eligibility determines which intents could apply in that context.
- Lifecycle hooks determine when eligibility should be reconsidered.
- Delivery policy determines whether and how guidance enters the context.
- Retraction contracts ensure guidance leaves when it is no longer useful.
- The engineering objective and its completion conditions bound every
  activation decision.
- A successful engineering objective completes before automatic transcript
  compaction is necessary.

## Keep sensing, eligibility, and activation separate

A file reference such as `src/main.rs` is an observation, not an activation
rule. It may contribute evidence for a reusable context such as
`context.language.rust`. An intent can then relate itself to that context
without repeating detector details.

This separation allows detectors to improve independently of the intent
catalogue and permits several observations to support the same context.

### Sensors and context nodes

Sensors may observe:

- paths read, written, edited, or returned by search tools;
- repository markers such as manifests and lockfiles;
- commands and their arguments;
- diagnostics, test failures, and static-analysis findings;
- the user's explicit language, framework, or activity references;
- the current engineering phase and recent agent actions.

A context node can combine several detectors with different confidence and
lifetimes. For example:

```toml
id = "context.language.rust"

[[detectors]]
kind = "tool-path"
glob = "**/*.rs"
operation = ["read", "write", "edit"]
confidence = 0.95

[[detectors]]
kind = "repository-file"
glob = "**/Cargo.toml"
confidence = 0.55

[[detectors]]
kind = "command"
pattern = "\\b(cargo|rustc|clippy|rustfmt)\\b"
confidence = 0.95
```

Observations should have strength, provenance, scope, and decay. Editing a
Rust source file is strong evidence for the current task. Merely finding a
Cargo manifest in a polyglot repository is weaker evidence. A path mentioned
by a search result should not carry the same weight as a path being edited.

### Intent-to-context relationships

Context relationships are distinct from semantic intent relationships such as
`specializes` and `related-to`.

```toml
[[contexts]]
relation = "requires"
target = "context.language.rust"

[[contexts]]
relation = "boosted-by"
target = "context.activity.static-analysis"

[[contexts]]
relation = "boosted-by"
target = "context.tool.clippy"

[[contexts]]
relation = "suppressed-by"
target = "context.activity.documentation-only"
```

Useful relationship types include:

- `requires` for a context without which the intent is ineligible;
- `boosted-by` for supporting evidence that raises its relevance;
- `suppressed-by` for evidence that makes injection less useful;
- `excludes` for a context that makes the intent inapplicable.

## Anchor activation to an engineering objective

The harness should maintain a compact, structured objective record rather
than reconstructing the objective from a compressed transcript:

```toml
[objective]
goal = "Add retry handling to outbound API calls"
done_when = [
  "Transient failures are retried with bounded backoff",
  "Permanent failures are returned immediately",
  "Relevant tests pass",
]
constraints = [
  "Do not change the public API",
]
```

An intent should be injected only when it helps satisfy a completion condition
or preserve a constraint. Once it no longer does so, it becomes a candidate
for retraction. The objective also gives the harness a stable basis for
detecting drift and determining whether the agent is converging.

## Lifecycle hooks

Lifecycle hooks tell the harness when to update sensors and reconsider a
small, relevant portion of the intent catalogue.

| Hook | Purpose |
| --- | --- |
| `objective-start` | Establish guidance for the agreed engineering outcome |
| `objective-complete` | Retract objective guidance and verify completion |
| `turn-start` | Interpret a new user instruction within the active objective |
| `phase-enter` | Activate investigation, implementation, or verification |
| `phase-exit` | Retract guidance owned by the completed phase |
| `context-gained` | Consider intents enabled by newly strong sensor evidence |
| `context-lost` | Retract intents whose supporting context has disappeared |
| `pre-tool-call` | Offer timely guidance before consequential operations |
| `post-tool-call` | React to diagnostics and other new evidence |
| `evidence-resolved` | Remove guidance associated with a resolved condition |
| `turn-end` | Check completion quality and unresolved risks |
| `budget-warning` | Reduce the working set and force convergence |
| `scope-failure` | Record why the objective exceeded its context budget |
| `agent-handoff` | Transfer active constraints and unfinished verification |

Tool-call hooks should be parameterized by operation rather than creating a
different hook for every tool. A pre-tool rule might apply only to edits of a
manifest, while a post-tool rule might react only to compiler or test output.

Pre-tool evaluation must be fast and narrowly indexed. It should not rescan
the entire catalogue before every action.

## Injection and retraction leases

Every injected intent should have a lease describing the scope that owns it,
the evidence that keeps it active, and the events that retract it.

```toml
[activation]
persistence = "phase"
inject_on = ["phase-enter", "context-gained"]
retract_on = ["phase-exit", "context-lost", "objective-complete"]
phases = ["implementation", "verification"]

[activation.threshold]
inject = 0.75
retract = 0.35
```

Different injection and retraction thresholds provide hysteresis. This keeps
guidance from flickering when sensor confidence moves around a single
boundary.

The harness should retain a compact activation receipt:

```text
intent: rust.quality.clippy
reason: Rust implementation phase; Cargo project detected
scope: phase
injected-at: tool-call 14
last-supported-at: tool-call 22
retract-when: implementation phase exits
```

The receipt supports deterministic retraction and prevents the same guidance
from being repeatedly injected. Re-injection is warranted only when relevant
context changes, evidence becomes stale, a new phase begins, or contradictory
evidence appears.

### Persistence classes

- `session` is fundamental harness policy and is rarely retractable.
- `objective` remains active for one engineering objective.
- `phase` remains active during a named phase of work.
- `contextual` remains active while sensor evidence is sufficiently strong.
- `operation` surrounds one tool call or short action sequence.
- `ephemeral` is consumed once and immediately retracted.

"Evergreen" describes broadly applicable guidance, not a separate lifecycle
hook. Most evergreen engineering guidance should have `objective` persistence,
be considered at `objective-start`, and be retracted at
`objective-complete`. Only fundamental harness policy should occupy the whole
session.

## Delivery policy

Activation does not always require a visible interruption. Delivery modes can
include:

- `silent-context` to make guidance available internally;
- `advisory` for a concise "before I do this" intervention;
- `checkpoint` to require a verification decision;
- `blocking` to prevent an operation until a condition is satisfied.

Most craftsmanship guidance should use `silent-context`. Visible advisories
should be brief and uncommon. Blocking delivery should be reserved for safety,
destructive operations, or explicit policy.

Each intent needs a compact runtime form so that selection does not require
injecting its full record:

```toml
[delivery]
mode = "advisory"
summary = "Keep Cargo manifests and lockfiles consistent."
max_tokens = 60
supersedes = ["quality.dependency-consistency"]
```

The full intent remains the authoritative explanation. The summary is the
small form used in a constrained working context.

Semantic graph relationships can reduce duplication. When a specialization is
active, it should normally supersede its generalized parent and irrelevant
siblings rather than adding to them.

## Runtime selection loop

At each lifecycle event, the harness should:

1. Run only the sensors relevant to that event.
2. Update a scored snapshot of current context.
3. Reconsider intents indexed by the changed contexts and lifecycle hook.
4. Rank eligible intents against the objective and available token budget.
5. Inject, retain, replace, or retract guidance according to its lease.
6. Record the activation decision and its supporting evidence.

A context snapshot might contain:

```text
language.rust = 0.96
activity.dependency-change = 0.88
tool.cargo = 1.00
phase.implementation = 0.82
```

Selection should prefer the most specific applicable intent and retain only
the generalized guidance that adds distinct value.

## Context budget and convergence

Context consumption should be controlled before the platform attempts
automatic compaction.

| Budget state | Harness response |
| --- | --- |
| Normal | Inject and retract according to relevance |
| Elevated | Retract dormant, redundant, and low-value guidance |
| High | Stop broad exploration and converge on the current objective |
| Critical | Declare scope failure before automatic compaction |

At elevated usage, the harness can remove guidance for inactive languages,
completed phases, resolved diagnostics, superseded generalized intents, and
completed operations. It should also discard stale observations and bulky tool
output that no longer supports a pending decision.

At high usage, the agent should finish the shortest valid path to the agreed
outcome. It should not silently redefine or subdivide the objective. If the
objective cannot be completed within the remaining budget, the agent should
report that explicitly.

## Compaction is a scope failure

Automatic transcript compaction is not part of the successful lifecycle. It
introduces compression loss and indicates that the harness failed to keep the
objective, exploration, evidence, or active guidance within bounds.

The operating invariant is:

> A successful engineering objective completes without automatic transcript
> compaction.

If the platform announces imminent compaction, the harness should emit a
`scope-failure` event rather than treating compaction as normal recovery. The
failure record should identify:

- the original objective and incomplete completion conditions;
- context consumed by guidance, tool output, exploration, and rework;
- intents that remained active longer than their useful lifetime;
- phases in which the agent failed to converge;
- whether the initial objective was under-scoped;
- the remaining work and unresolved risks.

This diagnostic can inform improvements to sensors, leases, objective sizing,
and agent behaviour without pretending that compressed context is equivalent
to the original working state.

## Evaluation and research metrics

Before enabling automatic injection, a trace-only selector should report what
it would inject or retract and why. Useful measures include:

- compaction-free objective completion rate;
- completion margin before the context limit;
- peak active-guidance tokens;
- guidance token-turns, combining guidance size and retention time;
- inject, refresh, supersede, and retract counts;
- irrelevant or late activations;
- context consumed before the first implementation action;
- context consumed after the objective was technically complete;
- unresolved leases at objective completion.

The first experiment can cover language contexts, the existing nested
ecosystems, activity contexts such as testing and dependency changes, and tool
contexts already represented by catalogue tags. It should produce an
explainable activation trace without yet changing the agent's context.

## Questions each intent must eventually answer

For an intent to participate safely in dynamic context management, its runtime
metadata must make these questions answerable:

- Why is this intent eligible now?
- Which objective, phase, context, or operation owns its activation?
- What evidence keeps it active?
- Which event or confidence change retracts it?
- Which more-specific intent supersedes it?
- How much context may it occupy?
- Should its delivery be silent, advisory, a checkpoint, or blocking?

These answers form the retraction contract that turns the intent graph from a
browsable catalogue into a manageable, live guidance system.
