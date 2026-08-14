# Generic harness implementation notes

These notes describe how to consume the intent library on agent platforms that
cannot dynamically inject and retract guidance during a session. Claude Code,
Codex, OpenCode, and similar tools may expose different configuration surfaces,
but they can share a platform-neutral process for assembling guidance.

The central idea is to treat an agent prompt or skill as a materialized,
cross-cutting slice through the intent graph. Intent records remain the source
of truth. Generated prompts and skills are delivery artifacts optimized for a
particular situation, context budget, and platform capability.

Materialization has two audiences that must not be confused. The build
mechanism needs selection rules, graph traversal records, source revisions, and
validation results. The working agent needs only guidance that can improve its
decisions. Build metadata belongs in an assembly record outside the agent's
context, not in the delivered prompt or skill.

This model complements the dynamic harness described in
[Harness implementation notes](HARNESS.md). A dynamic harness selects and
retracts intents continuously. A generic harness compiles likely-relevant
guidance ahead of time and relies on prompt scope, skill activation, and
progressive disclosure to control context.

## Two complementary delivery surfaces

Less controlled harnesses generally offer two useful ways to supply guidance:

1. A pre-loaded custom agent or repository prompt establishes a universal
   baseline for the full engineering objective.
2. Situational skills add deeper guidance, examples, tools, and procedures when
   their trigger conditions are present.

These are different products of the same intent library and should often be
used together.

| Surface | Best suited to | Context lifetime |
| --- | --- | --- |
| Baseline prompt | Invariants, posture, completion | Objective or session |
| Situational skill | Narrow domain or workflow guidance | While triggered |
| Skill reference | Examples, rationale, command matrices | On demand |
| Bundled script | Checks and repeatable transformations | During execution |

The materializer may produce an additional assembly record for operators and
build tooling. It is not a delivery surface and should never be loaded merely
because the agent uses the generated prompt or skill.

The baseline should make the agent reliably competent before any skill is
loaded. Skills should improve decisions in narrower situations rather than
repair omissions in the baseline's fundamental safety or completion contract.

## Baseline custom-agent guidance

A baseline prompt is expensive because it is always present. Include only
guidance with broad applicability and high cost of omission.

Good baseline candidates include:

- preserve the user's objective, constraints, and definition of done;
- inspect local conventions before changing code;
- keep changes cohesive and avoid speculative capability;
- verify behaviour in proportion to risk;
- report incomplete checks and unresolved risks honestly;
- protect user work and require clarity before destructive action;
- finish the objective before context exhaustion rather than relying on
  automatic compaction.

Poor baseline candidates include:

- commands for a particular package manager or test framework;
- language idioms irrelevant to most sessions;
- long examples and explanatory essays;
- exhaustive quality-tool matrices;
- framework-specific architecture rules;
- several equivalent formulations of the same principle.

The baseline is a compact operating constitution. It should describe durable
behaviour and completion semantics, not attempt to preload the whole catalogue.

## Situational skills

A skill is an ahead-of-time approximation of contextual activation. Its
description acts as a sensor: it tells the platform which user intentions,
artifacts, languages, tools, and activities should cause the skill to load.

A useful skill slice usually crosses several branches of the intent graph. For
example, a `rust-dependency-change` skill might combine:

- Rust and Cargo eligibility;
- dependency selection and version policy;
- manifest and lockfile consistency;
- vulnerability review;
- testing and static-analysis gates;
- documentation implications;
- examples of the expected commands and evidence.

This is more useful than generating one skill per elemental intent. Elemental
intents remain the composable source material; the skill represents a coherent
working situation an agent is likely to encounter.

### Skill trigger descriptions as coarse sensors

For platforms without tool-call sensing, skill metadata should encode the
strongest observable signals available to the model:

- user goals such as "upgrade a dependency" or "add an API endpoint";
- named languages, frameworks, and tools;
- artifact names such as `Cargo.toml`, `pyproject.toml`, or migration files;
- activity terms such as debugging, refactoring, documenting, or reviewing;
- common indirect phrasings that imply the same situation.

The description should say both what the skill enables and when to use it. It
should be broad enough to catch realistic phrasing but narrow enough to avoid
loading a large skill for adjacent work.

Trigger metadata is only a coarse sensor. The skill body should begin with a
small applicability check and gracefully stop or narrow itself when the
repository evidence does not support the assumed context.

### Progressive disclosure within a skill

Keep the primary skill instructions procedural and compact. Move material into
references when it is useful only under a further condition.

```text
rust-dependency-change/
├── SKILL.md
├── references/
│   ├── cargo-selection.md
│   ├── supply-chain-review.md
│   └── workspace-dependencies.md
└── scripts/
    └── inspect-dependency-state
```

The primary instructions should tell the agent exactly when to read each
reference. A repository with no Cargo workspace should not pay the context cost
of workspace-specific guidance.

Examples belong primarily in skill references. They deepen interpretation and
show how several elemental intents work together without making the universal
baseline larger.

References are not overflow storage for everything omitted from `SKILL.md`.
Include a reference only when the agent may benefit from choosing to read it
during the task. Assembly provenance, rejected candidates, graph diagnostics,
and validation reports belong to the materializer, not beside the skill as
agent-readable resources.

## Hybrid composition

The strongest generic configuration is often:

```text
universal baseline
  + project-local guidance
  + one activity skill
  + one language or ecosystem skill
  + references needed by the immediate decision
```

This composition approximates dynamic context management while using only
widely available platform features.

The baseline should not repeat the full text of skills. Instead, it can state
the expectation that the agent use applicable local skills and verify their
assumptions against repository evidence. Skills can assume the baseline's
general working contract but should remain understandable when used on their
own.

Avoid requiring two skills to activate in a precise order unless the target
platform guarantees composition semantics. When two slices are commonly
needed together, generate a deliberate combined profile or make one skill
self-sufficient through a small shared summary.

## Defining a cross-cutting slice

A materialization request should describe the situation, not merely list
files. Useful selection dimensions include:

- intended role or agent posture;
- engineering objective or activity;
- language and ecosystem eligibility;
- categories and topical tags;
- required and excluded contexts;
- graph relationships to traverse;
- desired delivery surface;
- maximum prompt or skill budget;
- desired depth of examples and rationale.

An illustrative materialization specification might look like:

```toml
id = "rust-dependency-change"
surface = "skill"
audience = "coding-agent"
budget_tokens = 2800

[select]
requires = ["context.language.rust"]
activities = ["dependency-change"]
categories = ["dependencies", "quality", "testing", "documentation"]
tags = ["cargo", "security", "lockfile"]

[graph]
follow = ["specializes", "related-to"]
max_related_depth = 1
prefer_specializations = true

[content]
include = ["guidance", "evidence", "examples"]
examples = "references"
```

This is a design sketch rather than a committed repository schema. Its purpose
is to make selection reproducible and reviewable. It is input to the
materializer, not content to copy into the generated skill.

## Slice compilation

A generic materializer should use a deterministic pipeline.

### 1. Establish the situation

Translate the requested profile into contexts, categories, tags, and activity
signals. Reject profiles that are so broad that they amount to exporting the
whole catalogue.

### 2. Select candidate intents

Select intents matching the required contexts and at least one meaningful
situational dimension. Category-only selection is usually too broad; combine
it with language, ecosystem, activity, tool, or artifact context.

### 3. Traverse the graph deliberately

- Follow `specializes` from general principles to applicable concrete forms.
- Include generalized parents only when they add distinct rationale or a
  durable invariant.
- Follow `related-to` conservatively and with a shallow depth limit.
- Exclude siblings whose eligibility context is absent.
- Record every traversal in the materializer's assembly report so generation
  is explainable without burdening the working agent.

### 4. Resolve overlap and precedence

Prefer the most specific applicable guidance. Merge compatible intents that
describe different parts of the same workflow. Surface contradictions rather
than silently choosing whichever record was encountered last.

The result should read as one coherent set of instructions, not as concatenated
intent records. Repeated principles should appear once, with specializations
supplying the concrete technique or tool.

### 5. Shape content for the delivery surface

For a baseline prompt:

- retain only high-value invariants;
- phrase guidance as durable operating behaviour;
- omit most examples, citations, and tool-specific detail;
- place completion and context-budget expectations prominently.

For a skill:

- write a strong trigger description;
- organize the body around the agent's workflow;
- provide applicability checks and stopping conditions;
- move only useful conditional details and examples into references;
- bundle deterministic procedures as scripts when that saves repeated
  reasoning.

Apply an agent-value test to every emitted token: would having this information
available change how the agent recognizes, performs, or verifies the task? If
not, keep it in the build system or omit it.

### 6. Fit the budget by value

Do not truncate generated guidance at an arbitrary token boundary. Rank content
by the cost of omission and compress it structurally:

1. Remove irrelevant examples and secondary related intents.
2. Replace repeated parents with a single shared principle.
3. Move conditional detail to references.
4. Condense rationale while preserving the decision it supports.
5. Fail generation if the remaining safety and completion contract cannot fit.

### 7. Write an assembly record

The materializer should retain build-time information separately from the
agent-facing artifact. An assembly record can contain:

- the materialization profile;
- source intent record keys and library revision;
- graph traversal and precedence decisions;
- excluded candidates and contradiction resolutions;
- output checksums and platform adapter version;
- validation results and warnings.

This record permits regeneration, review, staleness detection, and debugging.
It might be a lockfile, build manifest, or report stored with other generator
state. It should not be installed as a skill reference or injected into the
agent's prompt merely because the generator needs it.

The agent-facing output should contain provenance only when provenance itself
helps perform the task, such as an authoritative source the agent may need to
consult. A generated-file marker can live in packaging metadata or another
mechanism that does not consume working context.

### 8. Validate before delivery

Validation should check:

- all referenced intents and relationships exist;
- required contexts are represented in the trigger or applicability check;
- excluded contexts did not leak into the output;
- specializations do not duplicate their parents unnecessarily;
- the artifact fits its declared budget;
- platform metadata is valid;
- instructions contain no unresolved contradictions;
- links and bundled resources resolve.

Validation results belong in the assembly record or build output. Passing
validation should not add a validation narrative to the delivered guidance.

## Platform adapters

Keep selection and composition platform-neutral. A thin adapter should handle
the target platform's current file locations, frontmatter, discovery rules,
tool permissions, and naming conventions.

| Concern | Portable core | Platform adapter |
| --- | --- | --- |
| Guidance meaning | Selected intent slice | Prompt or skill syntax |
| Activation cues | Context and activity signals | Discovery conventions |
| Resource loading | Progressive-disclosure plan | Supported reference layout |
| Tool needs | Capability requirements | Tool names and permission syntax |
| Preloaded baseline | Baseline content | Repository or agent instructions |
| Build traceability | Assembly record | Generator-side manifest format |

Claude Code, Codex, and OpenCode should therefore receive semantically
equivalent artifacts without forcing the canonical intents to contain
platform-specific model names or configuration. The adapters may differ even
when the selected slice is identical.

Generated output should avoid depending on undocumented platform behaviour.
Where a platform lacks automatic skill triggering, the adapter can emit an
explicit invocation-oriented skill and a short baseline reminder about when to
use it. Where custom agents and skills can work together, the adapter should
keep their responsibilities distinct.

## Approximating lifecycle without live retraction

A static platform cannot truly retract pre-loaded guidance, but it can reduce
the cost of lifecycle mismatch:

- Put objective-lifetime guidance in the baseline.
- Put phase- or activity-lifetime guidance in separate skills.
- Put operation-specific detail in references or compact checklists.
- Tell a skill when its procedure is complete and when to stop consulting it.
- Prefer several coherent situational skills over one language megaskill.
- Start a fresh engineering objective rather than carrying an ever-growing
  conversation across unrelated work.

This is intentionally weaker than dynamic leases. The generic materializer
should describe the limitation honestly rather than pretending static prompt
composition provides retraction.

## Candidate materializations

The current catalogue could support useful slices such as:

- a universal craftsperson baseline;
- test-first feature implementation;
- dependency selection and upgrade review;
- quality-gate diagnosis and remediation;
- documentation synchronization;
- safe refactoring with behaviour preservation;
- repository-aware code review;
- language-specific implementation skills;
- ecosystem-specific skills such as Python with uv or Elixir with Phoenix;
- release-readiness verification;
- performance investigation without speculative optimization.

Some slices should be layered. A language skill can supply idioms and tool
defaults, while an activity skill supplies the workflow. A generated combined
profile can resolve overlap for platforms whose skill composition is weak or
unpredictable.

## Failure modes to avoid

### The language megaskill

Collecting every Rust or Python intent into one skill recreates the oversized
custom agents that the intent library is intended to decompose. Prefer
situational slices with language eligibility.

### The universal encyclopaedia

A baseline containing every general principle, rationale, tool, and example
consumes context regardless of relevance. Treat always-loaded tokens as the
most expensive delivery tier.

### Accidental forked truth

Hand-editing generated skills causes the same guidance to diverge across
platforms. Improve the source intents, materialization profile, or adapter and
regenerate. Enforce this through the build workflow and assembly record rather
than spending agent-visible tokens explaining the generator.

### Trigger-only correctness

A persuasive skill description does not guarantee that the assumed context is
real. Confirm repository evidence after activation before applying specialized
guidance.

### Hidden dependencies between skills

A skill should not silently rely on another skill having loaded. Make required
baseline assumptions explicit and generate combined profiles when ordering
matters.

### Examples mistaken for policy

Examples illustrate an intent under particular conditions. Preserve the
underlying decision and label conditional examples so they do not become
universal commands.

### Platform syntax in canonical intents

Embedding Claude Code, Codex, or OpenCode configuration directly in intent
records makes the library less portable. Keep platform syntax in adapters and
generated artifacts.

## Evaluation strategy

Evaluate the baseline, each skill, and their combination separately. Useful
comparisons include:

- no generated guidance;
- baseline only;
- skill only;
- baseline plus skill;
- broad language skill versus narrow situational skill;
- source slice before and after specialization resolution.

Test both activation and non-activation cases. A dependency skill should help
when a manifest changes and stay out of the way during unrelated documentation
work. Evaluation should examine outcome quality, triggering accuracy, context
cost, duplicated guidance, and whether the agent completes without unnecessary
exploration.

The materializer itself should also be deterministic: the same intent-library
revision and profile should produce the same semantic guidance, regardless of
the target platform adapter.

## Recommended first experiment

Start with one baseline and three narrow slices:

1. Generate a universal craftsperson baseline from high-value generalized
   intents.
2. Generate a dependency-change skill for one language ecosystem.
3. Generate a quality-gate remediation skill for that ecosystem.
4. Generate a documentation-synchronization skill that crosses languages.
5. Emit each artifact through Claude Code, Codex, and OpenCode adapters.
6. Compare baseline-only, skill-only, and combined behaviour on the same small
   engineering objectives.

This experiment tests the important boundaries: what deserves permanent
context, whether graph-derived skills form coherent workflows, how well
descriptions approximate sensors, and whether platform adapters preserve the
same intent without copying platform concerns into the library.
