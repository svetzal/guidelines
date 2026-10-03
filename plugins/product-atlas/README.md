# Product Atlas

Product Atlas creates a wiki that helps stakeholders understand a product.
It explains what the system does, what the product owner intends, and where
the two differ.

The repository must contain code, documentation, or both. Product Atlas reads
this material to build the wiki. It cannot work with an empty repository.

## Get started

Install `product-atlas` from the `svetzal-guidelines` plugin marketplace.
The plugin needs Python 3.9 or later.

1. Open your product repository.
2. Run `/product-atlas:generate-wiki`.
3. Provide the paths to code or documentation when asked.

The command saves your settings in `.product-atlas.json`. You can change these
settings to read from several repositories or store the files elsewhere.
Relative paths start from the directory that contains the settings file.

The default layout is:

```text
.product-atlas.json
product/
  intent/       What the product should do, and why
  questions/    Questions, answers, and earlier decisions
  generation/   Records of what the agent read and generated
  wiki/         The generated wiki
```

To prepare the settings yourself, copy [the template](templates/product-atlas.json).
Edit its product name and paths. To use another settings file, pass its path:

```text
/product-atlas:generate-wiki ./customer-product.json
```

## Record intent and answer questions

The plugin keeps two registries: one for product intent and one for questions.
Both are collections of Markdown files that you can read and edit.

Use these skills through ordinary conversation:

| Request | Skill |
| --- | --- |
| "Record this product decision." | `capture-product-intent` |
| "Ask me the unanswered questions." | `interview-product-owner` |
| "Does the code match our intent?" | `reconcile-product-evidence` |

When the agent finds a conflict, it checks for an existing question before
creating one. It can clarify a question without losing its answers or history.
Your answer can settle what the product should do even when the code still
needs to change. The wiki reports that remaining difference.

## Read and update the wiki

Start at `product/wiki/index.md`. The wiki describes who uses the product,
what they want to achieve, and how they use it. Links connect the actors,
goals, interactions, and journeys.

Each page explains what the agent found and which sources support it.
It distinguishes your stated intent from the agent's inferences.
With documentation alone, it describes documented behavior and identifies
what the agent could not check against the implementation.

Do not edit the generated wiki. Record corrections in the intent or question
registry. Run `/product-atlas:generate-wiki` again to update the wiki.

Generation replaces the whole wiki. It keeps your registries and source files.
If generation fails, it keeps the previous wiki too.

## Maintain the plugin

Run these checks from the guidelines repository root:

```sh
python3 -m unittest discover -s plugins/product-atlas/tests -v
claude plugin validate plugins/product-atlas
```

For the detailed rules, see [workspace settings](references/workspace.md),
[registry records](references/registries.md), and
[wiki generation](references/wiki.md).

The design builds on Stacey Vetzal's
[Screenplay Pattern extraction gist](https://gist.github.com/svetzal/716b963c631a3af1c0ebbe60b14cb32a/856646f41d5002dd52e0a6d582c716fdd3ac467f).
