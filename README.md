# Project Starters and Guidelines

Currently this is focused on Python projects.

I've been carrying around a number of "guidelines" files for Gen AI agents that is becoming cumbersome to manage. I've decided to create a centralized repository for these guidelines to make it easier for me to access and synchronize them.

There are two main markdown files containing agent guidance. The first (`guidelines.md`) is intended to be installed as each agent's baseline instructions:

- `.github/copilot-instructions.md`
- `.junie/guidelines.md`
- `CLAUDE.md`

The second (`starter.md`) is intended to be a prompt to give the agent in a fresh empty directory to have it generate a new project structure from scratch, that will be compatible with the guidelines.

## Layered Prompting Strategy

| Layer                                    | Purpose                                       | Maintainer    |
| ---------------------------------------- | --------------------------------------------- | ------------- |
| **0 - Project Identity & Context**       | One‑liner, elevator‑pitch, domain constraints | *per‑project* |
| **1 - Universal Engineering Principles** | Timeless software craft rules (below)         | **common**    |
| **2 - Language‑Specific Conventions**    | Language, tooling, ecosystem rules (below)    | **common**    |
| **3 - Framework-Specific Conventions**   | Usage conventions for a specific framework    | **common**    |
| **4 - Project‑Specific Extensions**      | Only additions / overrides; never duplicate   | *per‑project* |
