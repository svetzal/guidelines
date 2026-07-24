# Intent records

Intent records describe falsifiable engineering guidance. The
`craftsperson/` collection contains generalized intents; each
`*-craftsperson/` collection contains language or ecosystem specializations.

## Classification

Every record participates in the intent graph through three complementary
fields:

- `category` is the record's primary, stable area of concern.
- `tags` are lightweight topical facets, including named tools and techniques.
- `relations` are typed, directed edges to other intent records.

Relationship targets use the repository-relative record key
`<collection>/<slug>` without the `.toml` suffix. This avoids ambiguity because
the semantic `id` field may intentionally recur in more than one collection.

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

## Enrichment

Run the deterministic enrichment tool after adding or renaming ecosystem
records:

```bash
python3 site/enrich_intents.py
```

The tool inserts or replaces the classification block immediately after each
record's title. Existing prose, evidence, sources, and examples are preserved.
Review its changes as editorial content: the rules provide a consistent first
pass, not an excuse to skip domain judgment.
