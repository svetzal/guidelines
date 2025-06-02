# Project Starters and Guidelines

Generative AI agents all will take baseline guidelines to send with every task you give it. This can help with consistently in your project, and even with your own thinking around your project's code design by making them explicit and intentional.

## Origins

Currently this is focused on Python projects, because that's what I have most spinning around me right now. My intent is to grow it out to other languages and technologies (Node, Java, Elixir) as I have time, but this is where I'm at right now.

I've been carrying around a number of "guidelines" files for Gen AI agents that is becoming cumbersome to manage. I've decided to create a centralized repository for these guidelines to make it easier for me to access and synchronize them.

There are two main markdown files containing agent guidance. The first (`guidelines.md`) is intended to be installed as each agent's baseline instructions:

- `.github/copilot-instructions.md`
- `.junie/guidelines.md`
- `CLAUDE.md`

In `references/` you'll see where I copied in a few older guidelines files I have, in an attempt to distill things down and achieve consistently across all my Python projects.

The second (`starter.md`) is intended to be a prompt to give the agent in a fresh empty directory to have it generate a new project structure from scratch, that will be compatible with the guidelines.

## Layered Prompting Strategy

I can think of several more layers than this, but this is what I'm starting with. I realize as I write this I shouldn't have numbered them, but I'll fix that in a future iteration.

| Layer                                    | Purpose                                       | Maintainer    |
| ---------------------------------------- | --------------------------------------------- | ------------- |
| **0 - Project Identity & Context**       | One‑liner, elevator‑pitch, domain constraints | *per‑project* |
| **1 - Universal Engineering Principles** | Timeless software craft rules (below)         | **common**    |
| **2 - Language‑Specific Conventions**    | Language, tooling, ecosystem rules (below)    | **common**    |
| **3 - Framework-Specific Conventions**   | Usage conventions for a specific framework    | **common**    |
| **4 - Project‑Specific Extensions**      | Only additions / overrides; never duplicate   | *per‑project* |
