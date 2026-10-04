# Product Atlas

Product Atlas creates documentation that helps stakeholders understand a product.
It explains what the system does, what the product owner intends, and where
the two differ.

The repository must contain code, documentation, or both. Product Atlas reads
this material to build the documentation. It cannot work with an empty repository.

## Get started

Install `product-atlas` from the `svetzal-guidelines` plugin marketplace.
The plugin needs Python 3.9 or later.

1. Open your product repository.
2. Run `/product-atlas:generate-documentation`.
3. Provide the paths to code or documentation when asked.

The command saves your settings in `.product-atlas.json`. You can change these
settings to read from several repositories or store the files elsewhere.
Relative paths start from the directory that contains the settings file.

The default layout is:

```text
.product-atlas.json
product/
  intent/          Product intent, organized by topic
  questions/       Unresolved questions only
  history/         Earlier decisions, changes, and reviews
  documentation/   Generated documentation for stakeholders
```

To prepare the settings yourself, copy [the template](templates/product-atlas.json).
Edit its product name and paths. To use another settings file, pass its path:

```text
/product-atlas:generate-documentation ./customer-product.json
```

## Turn questions into intent

The agent records questions when purpose is unclear or the sources disagree.
It checks existing questions and intent before creating another question.

When you answer a question, the agent writes the meaning of your answer into
`intent/`. It records the change in `history/`, then deletes the answered question.
A partly answered question stays, with clearer wording about what remains unresolved.

Intent files group related decisions by topic. For example,
`intent/order-cancellation.md` can have sections for the cutoff, refunds, and
exceptions.

New answers refine those sections. The agent combines repeated ideas and
reorganizes topics as understanding improves.

Intent remains as a lasting statement of purpose after the code and documentation
match it. The agent keeps it succinct and removes duplication without changing
its meaning. Detailed discussions and earlier wording stay in `history/`.

Confirmed intent guides changes to the product. If code or documentation conflicts
with it, the agent asks about the desired behavior in plain language. The aim is
to bring the product into line with intent.

Intent can also describe what the product needs to do next. The implementation
may be behind. The documentation shows current behavior, intended behavior, and
what still needs to change. Clear, requested changes remain the direction for
implementation until the product owner changes that intent.

Use these skills through ordinary conversation:

| Request | Skill |
| --- | --- |
| "Record this product decision." | `capture-product-intent` |
| "Ask me the unanswered questions." | `interview-product-owner` |
| "Does the code match our intent?" | `reconcile-product-evidence` |

## Work toward no open questions

The goal is an empty `questions/` folder. After a current review, that means
implementation, documentation, and intent agree within the reviewed scope.
Their purpose is clear, with no known questions left to resolve.

An answer can clarify intent while the code still differs. The answered policy
question disappears, but a focused question tracks the remaining difference.
It closes when evidence shows alignment. A promised fix alone is not enough.

Missing evidence also leaves a question. With documentation alone, the agent can
explain the documented behavior, but cannot claim that the implementation matches.
Changes to code or intent can raise new questions on the next review.

## Read and update the documentation

Start at `product/documentation/index.md`. Links connect the actors, goals,
interactions, and journeys. Each page explains what the agent found and which
sources support it. It distinguishes your stated intent from the agent's inferences.

Do not edit the generated documentation. Record corrections in `intent/` or
`questions/`. Run `/product-atlas:generate-documentation` again to update it.

Generation replaces the whole documentation folder. It keeps your intent,
questions, history, and source files. If generation fails, it keeps the previous
output too. A question about outdated documentation remains until regeneration succeeds.

## Maintain the plugin

Run these checks from the guidelines repository root:

```sh
python3 -m unittest discover -s plugins/product-atlas/tests -v
claude plugin validate plugins/product-atlas
```

For the detailed rules, see [workspace settings](references/workspace.md),
[intent and questions](references/registries.md), and
[documentation generation](references/documentation.md).
Existing version 1 projects use [the upgrade steps](references/upgrade.md).

The design builds on Stacey Vetzal's
[Screenplay Pattern gist](https://gist.github.com/svetzal/716b963c631a3af1c0ebbe60b14cb32a/856646f41d5002dd52e0a6d582c716fdd3ac467f).
