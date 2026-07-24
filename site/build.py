#!/usr/bin/env python3
"""Build the static intent atlas site from every craftsperson intent record.

Stdlib only (requires Python 3.11+ for tomllib). Reads every intent record,
distills the fields the atlas presents, injects them into site/template.html,
and writes the finished page to _site/index.html for GitHub Pages.

Usage: python site/build.py [--out DIR]
"""

import argparse
import datetime
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTENTS_DIR = ROOT / "intents"
TEMPLATE = ROOT / "site" / "template.html"

ECOSYSTEM_RE = re.compile(r"plugins/([a-z-]+)-ecosystem/")


def load_intent(path: Path) -> dict:
    with path.open("rb") as f:
        record = tomllib.load(f)
    ecosystems = sorted(
        {
            m.group(1)
            for p in record.get("scope", {}).get("paths", [])
            if (m := ECOSYSTEM_RE.match(p))
        }
    )
    collection = path.parent.name
    return {
        "key": f"{collection}/{path.stem}",
        "slug": path.stem,
        "id": record["id"],
        "collection": collection,
        "kind": "general" if collection == "craftsperson" else "specialization",
        "title": record["title"],
        "category": record["category"],
        "tags": record.get("tags", []),
        "relations": [
            {
                "type": relation.get("type", "related-to"),
                "target": relation["target"],
            }
            for relation in record.get("relations", [])
        ],
        "confidence": record.get("confidence"),
        "status": record.get("status"),
        "capability": record.get("capability", ""),
        "threat": record.get("threat", ""),
        "expectation": record.get("expectation", ""),
        "strategy": record.get("strategy", ""),
        "tradeoff": record.get("tradeoff", ""),
        "evidence": [
            {
                "type": e.get("type", ""),
                "description": e.get("description", ""),
                "required": bool(e.get("required")),
            }
            for e in record.get("evidence", [])
        ],
        "ecosystems": ecosystems,
        "examples": {
            lang: {"good": ex.get("good", ""), "bad": ex.get("bad", "")}
            for lang, ex in record.get("examples", {}).items()
        },
    }


def build(out_dir: Path) -> Path:
    paths = sorted(
        path
        for collection in INTENTS_DIR.iterdir()
        if collection.is_dir()
        and (
            collection.name == "craftsperson"
            or collection.name.endswith("-craftsperson")
        )
        for path in collection.glob("*.toml")
    )
    intents = [load_intent(path) for path in paths]
    if not intents:
        sys.exit(f"no intent records found in {INTENTS_DIR}")
    keys = {intent["key"] for intent in intents}
    dangling = [
        f"{intent['key']} -> {relation['target']}"
        for intent in intents
        for relation in intent["relations"]
        if relation["target"] not in keys
    ]
    if dangling:
        sys.exit("dangling intent relationships:\n" + "\n".join(dangling))

    # `</` would terminate the inline <script> early if it ever appeared in data
    data = json.dumps(intents, separators=(",", ":")).replace("</", "<\\/")
    hljs = "\n".join(
        (ROOT / "site" / "vendor" / name).read_text()
        for name in ("highlight.min.js", "clojure.min.js", "elixir.min.js")
    )
    if "</script" in hljs.lower():
        sys.exit("vendored highlight.js would terminate the inline script tag")
    template = TEMPLATE.read_text()
    for marker in ("/*__DATA__*/", "/*__HLJS__*/", "__BUILT__"):
        if marker not in template:
            sys.exit(f"template is missing the {marker} marker")
    page = (
        template.replace("/*__DATA__*/", data)
        .replace("/*__HLJS__*/", hljs)
        .replace("__BUILT__", datetime.date.today().isoformat())
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.html"
    out.write_text(page)
    print(f"{len(intents)} intents -> {out}")
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "_site")
    build(parser.parse_args().out)
