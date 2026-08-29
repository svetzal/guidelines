# STE writing rules — the reasoning behind each area

The ASD-STE100 specification organizes its writing rules into nine areas. This
file paraphrases the intent of each area with examples, in original wording.
It is a working summary, not the specification — rule numbers, exact rule
text, and the controlled dictionary live in the official document
(free download from [asd-ste100.org](https://www.asd-ste100.org/)).

## 1. Words

The heart of STE: each approved word has one part of speech and one meaning.
"Close" is a verb ("close the valve"), so it cannot serve as an adjective
("do not go close to" becomes "do not go near"). "Follow" means "come after",
so a reader obeys instructions rather than following them. This sounds
pedantic until you watch a non-native reader hit "follow the procedure" and
wonder what comes after what.

Words outside the general vocabulary are still available in two categories:

- **Technical names** — nouns specific to your domain: the S3 bucket, the
  ingest queue, the firmware image. Keep them, and keep them consistent.
- **Technical verbs** — verbs of your craft: compile, deploy, reboot, flash.
  Same deal.

The discipline that transfers even without the dictionary: pick one term per
concept, use it everywhere, and never rotate synonyms for elegance. Synonym
variety is a virtue in essays and a defect in procedures.

## 2. Noun clusters

Stacks of nouns force the reader to guess the relationships between them.
"The next environment smoke test tooling repository" makes the reader parse
five nouns before finding the point. STE caps clusters at three words; break
longer ones with prepositions: "the tooling repository for the smoke tests in
the next environment". Longer, yes. Ambiguous, no.

When a long technical name is unavoidable, write it out once, give it a short
form, and use the short form after that.

## 3. Verbs

Use simple verb forms: past, present, future. Avoid "-ing" forms where an
infinitive or a noun works ("configuration" or "to configure", not
"configuring"). Write in the active voice — the passive hides the actor, and
in a procedure the actor is the reader. "The service should be restarted"
leaves open who restarts it; "Restart the service" does not.

Avoid phrasal verbs ("carry out", "set up" as a verb, "go over"). Their
meaning is not the sum of their words, which makes them a translation trap.
Each has a single-verb replacement: do, install, review.

## 4. Sentences

Procedural sentences carry at most 20 words; descriptive sentences at most
25. Long sentences are where second instructions hide. Keep the articles —
telegraphic style ("remove cover, check seal") reads faster to the writer and
slower to everyone else, because articles carry the signals that separate
nouns from verbs.

When a sentence enumerates more than three items, use a vertical list. The
list makes each item checkable; prose commas make them skimmable, and a
skimmed step is a skipped step.

## 5. Procedural writing

An instruction is a command: imperative form, active voice, one action.
"Remove the cover" — not "the cover is removed", "you should remove the
cover", or "removal of the cover". One instruction per sentence; if two
actions must happen, that is two sentences or two numbered steps. "And then"
joining two actions is the reliable smell.

Notes give information the reader needs to do the step correctly. They are
short, and they are not instructions in disguise — a note that says "the
service must be stopped first" should be the instruction "Stop the service"
one step earlier.

## 6. Descriptive writing

Description explains how something works so the reader can act on it later.
Paragraphs hold one topic and at most six sentences. Put the key information
first — the reader of documentation scans before they read. Present facts in
the order the reader meets them: what it is, what it does, what to do about
it.

## 7. Safety instructions

Warnings and cautions come before the step they protect, never after — a
reader who executes steps in order must meet the warning before the hazard.
Each one is a short command stating the risk and the required behavior:
"Do not run this script against the production database. Data deleted by this
script cannot be recovered." A warning buried mid-paragraph, or phrased as a
descriptive aside, is a warning the reader meets too late.

## 8. Punctuation and word counts

Punctuation carries meaning, so STE keeps it simple. Semicolons are out —
they join what should be two sentences. Colons introduce lists. Hyphenated
compounds and contractions count as their component words when you check
sentence length, so "don't" is two words and no length is saved by
contracting.

## 9. Writing practices

Rewriting existing prose into STE is its own craft. A word-for-word
substitution often produces a worse sentence than the original — the approved
replacement has a different shape, so rebuild the sentence around it. Work
top-down: split compound instructions first, convert to imperative and active
voice, then fix words, then fix clusters. Mechanical checks come last, and a
final human read catches what no checker sees: whether each sentence gives
the reader exactly one thing to do, and whether every term means the same
thing it meant on page one.
