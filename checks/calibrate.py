#!/usr/bin/env python3
"""Calibration gate for the validators under checks/.

A validator that cannot fail measures nothing. Every validator ships with
workspace fixtures it is expected to pass and to not pass, and this gate runs
each one exactly the way the verifier does — the entry point's absolute path,
`--workspace <fixture> --config <json-file>`, from the repository root — and
asserts the verdict `expected.json` records. Each run happens twice and the two
stdouts must be byte-identical, which is where the determinism rule is enforced.

    python3 checks/calibrate.py

Exit 0 when every row is green; 1 on any mismatch, crash, non-deterministic
output, validator without fixtures, or validator whose fixtures never expect
both a pass and a non-pass. Standard library only.
"""

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKS = ROOT / "checks"
FIXTURES = CHECKS / "fixtures"
NOT_LANGUAGES = {"fixtures", "lib", "rustfacts"}


def validators():
    """`{language: {slug: entry point}}` for every executable under checks/<language>/."""
    found = {}
    for directory in sorted(CHECKS.iterdir()):
        if not directory.is_dir() or directory.name in NOT_LANGUAGES:
            continue
        entries = {path.stem: path for path in sorted(directory.glob("*.py"))}
        if entries:
            found[directory.name] = entries
    return found


def fixture_sets(language):
    """Every `checks/fixtures/<language>/<name>/` holding an expected.json."""
    base = FIXTURES / language
    if not base.is_dir():
        return []
    sets = []
    for directory in sorted(base.iterdir()):
        expected = directory / "expected.json"
        if expected.is_file():
            sets.append((directory, json.loads(expected.read_text(encoding="utf-8"))))
    return sets


def invoke(entry, workspace, config_path):
    """One validator run, exactly as the verifier performs it."""
    return subprocess.run(
        [str(entry), "--workspace", str(workspace), "--config", str(config_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def state(verdict):
    """The three-state reading of a verdict, matching the verifier's table."""
    if not verdict.get("applicable", False):
        return "n/a"
    return "pass" if verdict.get("followed") else "fail"


def describe(expectation):
    return state(expectation) if "applicable" in expectation else "?"


def calibrate_one(entry, workspace, config_path, expectation):
    """A row: expected, actual, deterministic, and whether it is green."""
    first = invoke(entry, workspace, config_path)
    if first.returncode != 0:
        reason = next(
            (line for line in first.stderr.splitlines() if line.strip()), "no stderr"
        )
        return describe(expectation), f"exit {first.returncode}: {reason}", "-", False
    try:
        verdict = json.loads(first.stdout)
    except json.JSONDecodeError as error:
        return describe(expectation), f"unparseable stdout: {error}", "-", False

    second = invoke(entry, workspace, config_path)
    deterministic = second.returncode == 0 and second.stdout == first.stdout
    matched = all(verdict.get(key) == value for key, value in expectation.items())
    green = matched and deterministic
    return describe(expectation), state(verdict), "yes" if deterministic else "NO", green


def main():
    rows = []
    for language, entries in validators().items():
        seen = {slug: set() for slug in entries}
        for directory, expected in fixture_sets(language):
            config = expected.get("check_config", {})
            with tempfile.TemporaryDirectory() as scratch:
                config_path = pathlib.Path(scratch) / "config.json"
                config_path.write_text(json.dumps(config), encoding="utf-8")
                for slug, arms in sorted(expected.get("validators", {}).items()):
                    entry = entries.get(slug)
                    name = f"{language}/{slug}"
                    if entry is None:
                        rows.append(
                            (name, directory.name, "-", "?", "no such validator", "-", False)
                        )
                        continue
                    for arm, expectation in sorted(arms.items()):
                        workspace = directory / arm
                        if not workspace.is_dir():
                            wanted = describe(expectation)
                            missing = "fixture dir missing"
                            rows.append((name, directory.name, arm, wanted, missing, "-", False))
                            continue
                        wanted, got, deterministic, ok = calibrate_one(
                            entry, workspace, config_path, expectation
                        )
                        seen[slug].add(wanted)
                        rows.append((name, directory.name, arm, wanted, got, deterministic, ok))
        for slug, outcomes in sorted(seen.items()):
            if not outcomes:
                rows.append((f"{language}/{slug}", "-", "-", "-", "no fixtures", "-", False))
            elif "pass" not in outcomes or outcomes == {"pass"}:
                reason = "fixtures never expect both a pass and a non-pass"
                rows.append((f"{language}/{slug}", "-", "-", "-", reason, "-", False))

    print_table(rows)
    failures = [row for row in rows if not row[-1]]
    print()
    print(f"{len(rows) - len(failures)} of {len(rows)} rows green")
    return 1 if failures else 0


def print_table(rows):
    header = ("validator", "fixture", "arm", "expected", "actual", "deterministic", "result")
    table = [header] + [tuple(row[:-1]) + ("ok" if row[-1] else "MISMATCH",) for row in rows]
    widths = [max(len(str(line[column])) for line in table) for column in range(len(header))]
    for index, line in enumerate(table):
        cells = zip(line, widths, strict=True)
        print("  ".join(str(cell).ljust(width) for cell, width in cells).rstrip())
        if index == 0:
            print("  ".join("-" * width for width in widths))


if __name__ == "__main__":
    sys.exit(main())
