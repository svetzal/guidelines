# Product Atlas

Product Atlas helps stakeholders understand an existing system. Its generated
wiki explains what the implementation does, how that aligns with product
intent, and where the evidence disagrees.

It uses standalone file registries. It does not need Epilogue Tracker or a
hosted service. A code or documentation corpus is required. An empty project,
an intent registry, or an old generated wiki alone is not enough to run it.

## Start a product atlas

Install `product-atlas` from the `svetzal-guidelines` plugin marketplace.
Install the complete plugin. Its skills share references and a preflight script.
The plugin follows the repository's existing
[Claude plugin layout](https://code.claude.com/docs/en/plugins-reference).

1. Open a workspace for the product analysis.
2. Run `/product-atlas:generate-wiki`.
3. Supply the code or documentation paths when asked.

The command creates `.product-atlas.json` if no configuration exists. You can
also copy [the template](templates/product-atlas.json) and edit it first.
Paths resolve from the configuration file's directory. Absolute paths work too.
Multiple repositories and documentation-only analysis are supported.

```text
.product-atlas.json
product/
  intent/       Durable statements, rationale, and evidence
  questions/    Durable questions, answers, and decision history
  generation/   Source revisions, entity history, and run records
  wiki/         Replaceable stakeholder documentation
```

To select another configuration, pass its path:

```text
/product-atlas:generate-wiki ./customer-product.json
```

The only script dependency is Python 3.9 or later, using its standard library.
The agent reads sources and writes the wiki. The script checks configuration,
path boundaries, and candidate source files. A passing preflight does not prove
that those files contain useful product evidence. The agent must read them.

## Work with intent

| Request | Skill |
| --- | --- |
| "Record that customers must be able to cancel before dispatch." | `capture-product-intent` |
| "Ask me the most useful unanswered product questions." | `interview-product-owner` |
| "Check how this implementation aligns with our intent." | `reconcile-product-evidence` |

Skills record durable information and report when the wiki needs regeneration.
They do not edit wiki pages. Answers can settle intent while an implementation
gap remains open in the drift report.

Questions have stable IDs. Matching uses the underlying decision, actor, goal,
and scope, rather than the wording alone. Clarifying a question preserves its
history. Repeated evidence of the same gap does not create another question.

## Read the wiki

Start at `wiki/index.md`. Follow links through actors, goals, interactions, and
journeys. Each page separates implementation evidence, recorded intent, inferred
intent, alignment, and unanswered questions.

The index states what was inspected and what could not be verified. With only
documentation, the wiki describes documented behavior and explicitly says that
the current implementation has not been verified.

The generated `AGENTS.md` and page notices direct corrections to the registries.
These are agent instructions, not a filesystem access control. Regeneration
replaces the complete wiki, including stale files. Sources and registries are
outside that replacement boundary. Failed generation preserves the previous wiki.

## Maintenance

Run the checks from this repository's root:

```sh
python3 -m unittest discover -s plugins/product-atlas/tests -v
claude plugin validate plugins/product-atlas
```

The shared contracts are in [workspace.md](references/workspace.md),
[registries.md](references/registries.md), and [wiki.md](references/wiki.md).
The design adapts Stacey Vetzal's
[Screenplay Pattern extraction gist](https://gist.github.com/svetzal/716b963c631a3af1c0ebbe60b14cb32a/856646f41d5002dd52e0a6d582c716fdd3ac467f).
