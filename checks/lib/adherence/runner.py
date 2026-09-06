"""The shared validator entry point behind every `checks/<language>/<slug>.py`.

A validator is invoked by the verifier as

    <knowledge-base-root>/checks/<language>/<slug>.py --workspace <root> --config <json-file>

and answers with exactly one JSON document on stdout, exit 0: `applicable`,
`followed`, `signals`, `evidence`, `locations`. Everything else — a missing
extractor, an unreadable workspace, a config the check cannot use — is a
nonzero exit with the reason as the first line of stderr, which the verifier
records as *unchecked*. A verdict is never printed unless it was computed.
"""

import argparse
import json
import pathlib
import sys

from . import rustfacts
from .checks import CHECKS
from .workspace import Workspace


def main(intent, language):
    """Parse the protocol arguments, run `intent`'s check, print the verdict."""
    parser = argparse.ArgumentParser(
        prog=f"checks/{language}/{intent.rsplit('/', 1)[-1]}.py",
        description=f"Deterministic {language} validator for {intent}.",
    )
    parser.add_argument("--workspace", required=True, type=pathlib.Path, help="project root")
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        help="JSON file holding this intent's project configuration (default: empty)",
    )
    arguments = parser.parse_args()

    try:
        verdict = run(intent, language, arguments.workspace, arguments.config)
    except Exception as error:  # the process boundary: any failure is "no verdict"
        sys.stderr.write(f"{intent}: {type(error).__name__}: {error}\n")
        return 1

    json.dump(verdict, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0


def run(intent, language, root, config_path):
    """The verdict for one intent over one workspace."""
    check = CHECKS.get(intent)
    if check is None:
        raise LookupError(f"no check implements {intent}")
    if not root.is_dir():
        raise NotADirectoryError(f"workspace {root} is not a directory")
    config = load_config(config_path)
    binary = rustfacts.locate(config) if language == "rust" else None
    workspace = Workspace(root, language=language, rustfacts=binary)
    return check(workspace, config)


def load_config(path):
    if path is None:
        return {}
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError(f"--config {path} must hold a JSON object")
    return document
