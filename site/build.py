#!/usr/bin/env python3
"""Build the static intent atlas site from intents/craftsperson/*.toml.

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
INTENTS_DIR = ROOT / "intents" / "craftsperson"
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
    return {
        "slug": path.stem,
        "title": record["title"],
        "category": record["category"],
        "tags": record.get("tags", []),
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
    }


def build(out_dir: Path) -> Path:
    intents = [load_intent(p) for p in sorted(INTENTS_DIR.glob("*.toml"))]
    if not intents:
        sys.exit(f"no intent records found in {INTENTS_DIR}")

    # `</` would terminate the inline <script> early if it ever appeared in data
    data = json.dumps(intents, separators=(",", ":")).replace("</", "<\\/")
    template = TEMPLATE.read_text()
    for marker in ("/*__DATA__*/", "__BUILT__"):
        if marker not in template:
            sys.exit(f"template is missing the {marker} marker")
    page = template.replace("/*__DATA__*/", data).replace(
        "__BUILT__", datetime.date.today().isoformat()
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
