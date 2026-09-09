#!/usr/bin/env python3
"""Validator for craftsperson/python/functional-core-imperative-shell.

The modules carrying the project's business rules import no filesystem,
network, database, or process library, and the external call is made from a
module that carries none of those rules.

A thin entry point: the check itself lives in ../lib/adherence/checks.py and
the invocation protocol in ../README.md.
"""

import pathlib
import sys

INTENT = "craftsperson/python/functional-core-imperative-shell"
LANGUAGE = "python"


def main():
    # Never write bytecode into the knowledge-base tree: a verifier may run
    # this from a scratch copy of a pinned revision.
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "lib"))
    from adherence import runner

    return runner.main(INTENT, LANGUAGE)


if __name__ == "__main__":
    sys.exit(main())
