#!/usr/bin/env python3
"""Merge per-language code-example fragments into the intent TOML records.

Fragments live in a directory as <lang>.json, each shaped:
    {"<intent-slug>": {"good": "<code>", "bad": "<code>"}, ...}

Each intent file's examples live below a marker comment as
[examples.<lang>] tables. This script rewrites everything below the
marker from the fragments, so re-running is idempotent. Fragments only
add or replace languages they contain; other languages already present
in a record are preserved.

Usage: python site/merge_examples.py <fragments-dir>
"""

import argparse
import sys
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTENTS_DIR = ROOT / "intents" / "craftsperson"
MARKER = "# --- code examples (rendered by the intent atlas; managed by site/merge_examples.py) ---"


def toml_multiline(s: str) -> str:
    s = s.rstrip("\n")
    if "'''" not in s:
        return "'''\n" + s + "\n'''"
    escaped = s.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    return '"""\n' + escaped + '\n"""'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fragments", type=Path)
    args = parser.parse_args()

    fragments: dict[str, dict] = {}
    for path in sorted(args.fragments.glob("*.json")):
        fragments[path.stem] = json.loads(path.read_text())
    if not fragments:
        sys.exit(f"no *.json fragments in {args.fragments}")

    intent_files = {p.stem: p for p in sorted(INTENTS_DIR.glob("*.toml"))}
    for lang, entries in fragments.items():
        unknown = sorted(set(entries) - set(intent_files))
        if unknown:
            sys.exit(f"{lang}.json refers to unknown intents: {unknown}")
        missing = sorted(set(intent_files) - set(entries))
        if missing:
            print(f"note: {lang}.json lacks {len(missing)} intents: "
                  + ", ".join(missing))

    for slug, path in intent_files.items():
        text = path.read_text()
        head = text.split(MARKER)[0].rstrip("\n")
        existing = tomllib.loads(text).get("examples", {})
        merged = dict(existing)
        for lang, entries in fragments.items():
            if slug in entries:
                merged[lang] = {
                    "good": entries[slug]["good"],
                    "bad": entries[slug]["bad"],
                }
        if not merged:
            continue

        blocks = [head, "", MARKER]
        for lang in sorted(merged):
            blocks.append(f"\n[examples.{lang}]")
            blocks.append(f"good = {toml_multiline(merged[lang]['good'])}")
            blocks.append(f"bad = {toml_multiline(merged[lang]['bad'])}")
        out = "\n".join(blocks) + "\n"

        parsed = tomllib.loads(out)  # raises on malformed output
        assert set(parsed["examples"]) == set(merged)
        path.write_text(out)

    langs = ", ".join(sorted(fragments))
    print(f"merged {len(fragments)} language(s) [{langs}] "
          f"into {len(intent_files)} intent records")


if __name__ == "__main__":
    main()
