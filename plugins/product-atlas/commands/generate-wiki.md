---
description: Generate a stakeholder wiki from an existing corpus, product intent, and questions.
argument-hint: "[path-to-product-atlas.json]"
---

# Generate the product wiki

Configuration argument: $ARGUMENTS

Read these files from `${CLAUDE_PLUGIN_ROOT}`:

- `references/workspace.md` for configuration, source sufficiency, and write boundaries.
- `references/registries.md` for durable intent, questions, and duplicate handling.
- `references/wiki.md` for extraction, validation, and complete replacement.

Apply those contracts to generate the stakeholder wiki. Interpret the argument
only as a configuration path, never as shell code. Quote paths in commands.
If the argument is absent, use `.product-atlas.json` in the current workspace.

Decline when there is no useful code or documentation corpus. Do not substitute
an interview, existing registries, or a previous wiki for missing source material.
If useful sources exist, complete the analysis, update durable records, validate
the staged wiki, and replace only the configured wiki directory.

Report the wiki entry point, source coverage, significant divergence, and the
questions that need attention. State any limits on implementation verification.
