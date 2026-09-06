# Intent records

Intent records describe falsifiable engineering guidance. The
`craftsperson/` collection contains generalized intents at its root and
language or ecosystem specializations in nested directories. The directory
hierarchy denotes the realization hierarchy: for example,
`craftsperson/cpp-qt/` specializes the general craftsperson catalogue for
C++/Qt, while `craftsperson/python/uv/` specializes Python guidance for uv-based
projects.

Implementation models:

- [Dynamic harness notes](HARNESS.md) cover sensing, selecting, injecting, and
  retracting intents during an agent session.
- [Generic harness notes](GENERIC.md) cover compiling cross-cutting slices into
  baseline prompts and situational skills for Claude Code, Codex, OpenCode, and
  similar platforms.

## Classification

Every record participates in the intent graph through three complementary
fields:

- `category` is the record's primary, stable area of concern.
- `tags` are lightweight topical facets, including named tools and techniques.
- `relations` are typed, directed edges to other intent records.

Relationship targets use the repository-relative record key
`<collection>/<slug>` without the `.toml` suffix. Collections may be nested,
such as `craftsperson/python/uv`. This avoids ambiguity because the semantic
`id` field may intentionally recur in more than one collection.

```toml
category = "quality"
tags = ["static-analysis", "ruff", "warnings"]

[[relations]]
type = "specializes"
target = "craftsperson/resolve-static-analysis-findings"
```

Use `specializes` when a record makes a general intent concrete for a language,
framework, tool, or narrower operating context. Use `related-to` for a
meaningful non-hierarchical association. A record may have more than one
relationship; the graph is not a tree.

Categories organize the catalogue and provide large-scale landmarks in the
graph. Tags connect intents laterally. Neither replaces an explicit
relationship when one intent is a recognizable specialization of another.

## Static-check evidence

An `evidence` entry of type `static-check` names an executable validator that
decides, from a project's source alone, whether the code holds the intent. It
carries `language` (the source language it reads) and `run` (a path relative to
the repository root, under `checks/`) alongside the `description` and `required`
every evidence entry has. The description is what an agent sees in compiled
guidance, so it states the observable expectation the check enforces. The
validators, their protocol, and the calibration fixtures that prove each one can
both pass and fail are documented in [checks/README.md](../checks/README.md).

## Enrichment

Run the deterministic enrichment tool after adding or renaming ecosystem
records:

```bash
python3.11 site/enrich_intents.py
```

The tool inserts or replaces the classification block immediately after each
record's title. Existing prose, evidence, sources, and examples are preserved.
Review its changes as editorial content: the rules provide a consistent first
pass, not an excuse to skip domain judgment.
