---
name: simplified-technical-english
description: >
  Write and review technical documentation to the principles of ASD-STE100 Simplified Technical
  English — the controlled-language standard that keeps procedures unambiguous for stressed readers
  and non-native English speakers. Use this skill whenever writing, reviewing, or rewriting a
  runbook, playbook, procedure, install or migration guide, troubleshooting steps, safety warnings,
  technical README, or any numbered instructions a person will follow. Also use it when asked what
  to use instead of a word like "ensure" or "utilize", whether sentences are too long, or to check
  a document for controlled-language compliance. Trigger on "STE", "ASD-STE100", "Simplified
  Technical English", "controlled language", "make this procedure clearer", "tighten up this
  runbook", or any request to make instructions easy for a non-native speaker to follow — even if
  the user never names the standard.
license: MIT
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---

# Simplified Technical English

ASD-STE100 is a controlled-language specification from the AeroSpace and Defence
Industries Association of Europe. It exists because the reader of a procedure is
often tired, working in a second language, and unable to ask a follow-up
question. STE removes the ambiguity that ordinary technical prose carries
without noticing: words with several meanings, sentences that hide two
instructions, and noun stacks nobody can parse on first read.

This skill applies STE's principles. It deliberately does not reproduce the
specification — see "The official specification" below.

## What STE binds

Apply it to text a reader follows under pressure or returns to weeks later:
playbooks, runbooks, procedures, validation documents, technical READMEs,
install and migration guides, troubleshooting steps, and safety warnings.

Do not apply it to conversational messages, correspondence, blog posts, or
marketing copy. Those need warmth and register-matching that STE's imperative
directness would flatten. When a conversational message contains a numbered
procedure, apply STE to the steps and normal tone to everything around them.

## The nine rules that carry the weight

You do not need the full specification in context. These nine rules catch most
problems, and the checker script finds the mechanical remainder.

1. One instruction per sentence. Split anything joined by "and then".
2. Maximum 20 words in a procedural sentence, 25 in a descriptive one.
3. Active voice. "Close the valve", not "the valve should be closed".
4. Imperative form for instructions. "Remove the cover", not "the cover is
   removed".
5. One word, one meaning. Pick one term per concept and repeat it. Never rotate
   synonyms for variety — "the deploy script" stays "the deploy script", not
   "the release tool" two paragraphs later.
6. Keep the articles. "Remove the cover", not telegraphic "remove cover".
7. Maximum three words in a noun cluster. Break longer stacks with
   prepositions: "the tooling repo for the smoke tests", not "the smoke test
   tooling repo".
8. Maximum six sentences per paragraph, one topic per paragraph. Use a vertical
   list when a sentence enumerates more than three items.
9. Warnings and cautions come before the step they modify, as short standalone
   commands. "Do not run this against production. Run the script against the
   test tables."

## Common word substitutions

STE's dictionary gives each approved word one part of speech and one meaning.
These substitutions come up constantly in engineering documentation:

| Instead of | Write |
| --- | --- |
| ensure, verify | make sure, do a check of |
| utilize, leverage | use |
| perform, carry out, execute (a step) | do |
| prior to | before |
| subsequent to, following (prep.) | after |
| in order to | to |
| commence, initiate | start |
| terminate, cease | stop |
| sufficient | enough |
| approximately | approximately is fine spelled out; prefer "about" |
| attempt (verb) | try |
| additional | more |
| assist | help |
| observe (see) | see |
| indicate | show |
| require | need, or "must" restructured |
| in the event of | if |
| at this point in time | now |
| follow (obey) | obey — "obey the instructions"; "follow" means "come after" |
| close (adjective) | near — "close" is the verb: "close the valve" |

Two cautions. First, a straight word swap often breaks the sentence — rebuild
the sentence around the replacement instead of forcing it. Second, a word
absent from this table is not automatically wrong: STE lets you keep
domain-specific technical names (the API endpoint, the S3 bucket) and technical
verbs (compile, deploy, reboot) that ordinary dictionaries would not carry.
The one-meaning discipline still applies — use each technical term one way.

## Checking a document

```bash
python3 scripts/ste_check.py DOCUMENT.md
```

The checker is deterministic and reports `file:line [check] message`. It finds
long sentences, "and then" chains, semicolons, overlong paragraphs, passive
voice, noun clusters, and the common non-STE words above. Exit code is 1 when
findings exist, so it works as a CI or pre-commit gate. `--json` emits
structured findings for scripting.

Passive-voice and noun-cluster findings are heuristics — they need a
part-of-speech tagger to be exact, so read each one before acting on it. The
rest are mechanical and can be trusted.

The checker cannot see the judgement rules. One instruction per sentence, one
word per concept, and warning placement still need you to read the text.

## Rewriting non-STE text

Work in this order:

1. Split compound instructions into one instruction per sentence.
2. Convert to the imperative and the active voice.
3. Replace non-approved words, rebuilding the sentence where needed.
4. Break noun clusters longer than three words.
5. Run the checker and resolve what it finds.
6. Read the result once for the judgement rules the checker cannot see.

Watch for phrasal verbs on the way through ("carry out", "set up" as a verb,
"make sure to go over") — STE mostly forbids them because their meaning is not
the sum of their words. Replace each with a single verb ("do", "install",
"read").

For the reasoning behind each rule area, with examples, read
`references/writing-rules.md`.

## The official specification

ASD-STE100 is copyright ASD and is a free download from
[asd-ste100.org](https://www.asd-ste100.org/) after registration. This skill
paraphrases the principles and does not reproduce the specification's rule text
or its controlled dictionary (about 900 approved general words plus several
thousand unapproved entries with alternatives). For word-level authority — is
this exact word approved, in which part of speech, with which meaning —
download the specification and check the dictionary directly. The skill's
substitution table above covers the cases engineering documentation hits most
often, not the full vocabulary.
