#!/usr/bin/env python3
"""Check a document against the mechanical rules of ASD-STE100.

The checks are deterministic and cheap. They catch what a machine can see:
sentence length, "and then" chains, semicolons, paragraph length, passive
voice, noun clusters, and a curated list of common non-STE words. Judgement
rules such as "one instruction per sentence" still need a person or an agent
reading the text.

This script is self-contained. It paraphrases STE principles and does not
embed the ASD-STE100 dictionary, which is ASD copyright. For word-level
authority, download the specification from https://www.asd-ste100.org/.

  ste_check.py DOCUMENT.md            flag mechanical violations
  ste_check.py DOCUMENT.md --json     same, as JSON
  ste_check.py A.md B.md              check several files

Exit code is 1 when findings exist, so the script works as a gate.
"""

import argparse
import json
import re
import sys
from pathlib import Path

PROCEDURAL_LIMIT = 20
DESCRIPTIVE_LIMIT = 25
PARAGRAPH_LIMIT = 6

# Words that commonly open an instruction. Used only to decide which sentence
# length limit applies; not a claim about the STE dictionary.
IMPERATIVE_OPENERS = set("""
add apply check clean click close configure confirm connect copy create delete
disable disconnect do download edit enable enter examine export find flush get
import insert install keep list load lock log make monitor move obey open
paste pause press pull push put read reboot remove rename repeat replace
restart restore resume review run save select send set show shut start stop
tap test try turn type unlock update upload use verify wait write
""".split())

# Small words that never form part of a noun cluster.
FUNCTION_WORDS = set("""
a an the and or but nor if of in on to for with from at by as into onto than
then that this these those is are was were be been being am can could do does
did done not no so such only just also very too much many more most some any
all each every both either neither other another same own few less least you
your it its they them their we our i me my he she him her his who whom whose
which what when where why how while after before during between through above
below over under about against across along among around behind beyond despite
except inside outside since toward towards until upon within without because
although though unless whether here there now always never often sometimes
usually already still yet again however therefore thus otherwise instead
rather have has had having will would shall should may might must
""".split())

BE_FORMS = {"is", "are", "was", "were", "be", "been", "being"}
PARTICIPLE = re.compile(r"^\w+(ed|en|wn|ne|ilt|ent|eft|ost|ung)$", re.IGNORECASE)
# Adjectives and nouns whose endings look like participles but are not.
NOT_PARTICIPLES = set("""
open often even seven eleven dozen wooden golden sudden hidden screen kitchen
current present frequent recent silent urgent absent adjacent different
independent permanent transparent consistent persistent red need speed
""".split())

# Common non-STE words in engineering documentation, with replacements. A
# curated example list, not the controlled dictionary.
WORD_CHOICE = {
    "ensure": "make sure",
    "verify": "make sure, or 'do a check of'",
    "utilize": "use",
    "utilise": "use",
    "leverage": "use",
    "perform": "do",
    "execute": "do (for a step; 'run' a program is a technical verb)",
    "commence": "start",
    "initiate": "start",
    "terminate": "stop",
    "cease": "stop",
    "sufficient": "enough",
    "attempt": "try",
    "additional": "more",
    "assist": "help",
    "indicate": "show",
    "prior": "before (for 'prior to')",
    "subsequent": "after (for 'subsequent to')",
    "approximately": "about",
    "demonstrate": "show",
    "facilitate": "help, or rebuild the sentence",
    "modification": "change",
    "modifications": "changes",
    "functionality": "function, or name the behavior",
    "aforementioned": "name the thing again",
    "via": "with, through, or by",
}

PHRASES = {
    "and then": "split into two instructions",
    "in order to": "to",
    "prior to": "before",
    "subsequent to": "after",
    "in the event of": "if",
    "at this point in time": "now",
    "carry out": "do",
    "make sure to": "a direct instruction ('Do X.', with 'Make sure that' for conditions)",
}

FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^\s*#")
TABLE_ROW = re.compile(r"^\s*\|")
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")


def sentences(text):
    """Split prose into sentences. Crude but adequate for checking."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if WORD.search(p)]


def words(sentence):
    return WORD.findall(sentence)


def clean(line):
    line = INLINE_CODE.sub("code", line)
    line = LINK_TARGET.sub("]", line)
    return line


def base_form(token):
    """Reduce an inflected form to a base the word-choice table may hold."""
    for strip in ("ing", "ed", "es", "s", "d"):
        if token.endswith(strip) and len(token) - len(strip) >= 4:
            stem = token[: -len(strip)]
            for candidate in (stem, stem + "e"):
                if candidate in WORD_CHOICE:
                    return candidate
    return token


def check_sentence(sent, findings, path, lineno):
    toks = words(sent)
    lowered = [t.lower() for t in toks]
    if not toks:
        return

    procedural = lowered[0] in IMPERATIVE_OPENERS
    limit = PROCEDURAL_LIMIT if procedural else DESCRIPTIVE_LIMIT
    if len(toks) > limit:
        kind = "procedural" if procedural else "descriptive"
        findings.append((path, lineno, "sentence-length",
                         f"{len(toks)} words in a {kind} sentence (limit {limit}): "
                         f"\"{sent[:60]}...\""))

    for i, tok in enumerate(lowered):
        if tok in BE_FORMS and i + 1 < len(lowered):
            nxt = lowered[i + 1]
            if (PARTICIPLE.match(nxt) and nxt not in FUNCTION_WORDS
                    and nxt not in NOT_PARTICIPLES):
                findings.append((path, lineno, "passive-voice",
                                 f"possible passive: \"{toks[i]} {toks[i + 1]}\" "
                                 "(heuristic — read before acting)"))
                break

    run = 0
    start = 0
    for i, tok in enumerate(lowered):
        if i == 0 and procedural:
            continue  # the leading verb of an instruction is not part of a cluster
        if tok in FUNCTION_WORDS or not tok.isalpha():
            run = 0
        else:
            if run == 0:
                start = i
            run += 1
            if run == 4:
                cluster = " ".join(toks[start:start + 4])
                findings.append((path, lineno, "noun-cluster",
                                 f"possible 4+ word cluster: \"{cluster}\" "
                                 "(heuristic — read before acting)"))
                run = 0

    seen = set()
    for tok in lowered:
        base = tok if tok in WORD_CHOICE else base_form(tok)
        if base in WORD_CHOICE and base not in seen:
            seen.add(base)
            shown = base if base == tok else f"{tok} ({base})"
            findings.append((path, lineno, "word-choice",
                             f"\"{shown}\" — prefer: {WORD_CHOICE[base]}"))


def check_heading(text, findings, path, lineno):
    """Headings are not sentences, but the noun-cluster and word-choice rules
    still apply — a title is the first thing a scanning reader parses."""
    toks = words(clean(text))
    lowered = [t.lower() for t in toks]
    skip_first = bool(lowered) and lowered[0] in IMPERATIVE_OPENERS

    run = 0
    start = 0
    for i, tok in enumerate(lowered):
        if i == 0 and skip_first:
            continue
        if tok in FUNCTION_WORDS or not tok.isalpha():
            run = 0
        else:
            if run == 0:
                start = i
            run += 1
            if run == 4:
                cluster = " ".join(toks[start:start + 4])
                findings.append((path, lineno, "noun-cluster",
                                 f"possible 4+ word cluster in heading: \"{cluster}\" "
                                 "(heuristic — read before acting)"))
                run = 0

    seen = set()
    for tok in lowered:
        base = tok if tok in WORD_CHOICE else base_form(tok)
        if base in WORD_CHOICE and base not in seen:
            seen.add(base)
            shown = base if base == tok else f"{tok} ({base})"
            findings.append((path, lineno, "word-choice",
                             f"\"{shown}\" in heading — prefer: {WORD_CHOICE[base]}"))


def check_file(path):
    findings = []
    in_fence = False
    para_sentences = 0
    para_start = 0

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if not in_fence and HEADING.match(raw):
            check_heading(raw.lstrip(" #"), findings, str(path), lineno)
            continue
        if in_fence or TABLE_ROW.match(raw):
            continue

        line = clean(raw)
        stripped = line.strip()

        if not stripped:
            if para_sentences > PARAGRAPH_LIMIT:
                findings.append((str(path), para_start, "paragraph-length",
                                 f"{para_sentences} sentences in one paragraph "
                                 f"(limit {PARAGRAPH_LIMIT})"))
            para_sentences = 0
            continue

        if para_sentences == 0:
            para_start = lineno
        is_list_item = bool(LIST_ITEM.match(raw))
        body = LIST_ITEM.sub("", stripped) if is_list_item else stripped
        sents = sentences(body)
        if not is_list_item:
            para_sentences += len(sents)

        if ";" in body:
            findings.append((str(path), lineno, "semicolon",
                             "semicolon — split into two sentences or use a list"))
        lower = body.lower()
        for phrase, fix in PHRASES.items():
            if phrase in lower:
                findings.append((str(path), lineno, "phrase",
                                 f"\"{phrase}\" — prefer: {fix}"))

        for sent in sents:
            check_sentence(sent, findings, str(path), lineno)

    if para_sentences > PARAGRAPH_LIMIT:
        findings.append((str(path), para_start, "paragraph-length",
                         f"{para_sentences} sentences in one paragraph "
                         f"(limit {PARAGRAPH_LIMIT})"))
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true", help="emit findings as JSON")
    args = ap.parse_args()

    findings = []
    for path in args.files:
        if not path.exists():
            print(f"error: {path} does not exist", file=sys.stderr)
            return 2
        findings.extend(check_file(path))

    if args.json:
        print(json.dumps([
            {"file": f, "line": n, "check": c, "message": m}
            for f, n, c, m in findings
        ], indent=2))
    else:
        for f, n, c, m in findings:
            print(f"{f}:{n} [{c}] {m}")
        if not findings:
            print("clean — no mechanical findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
