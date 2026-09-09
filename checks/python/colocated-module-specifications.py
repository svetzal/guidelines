#!/usr/bin/env python3
"""Validator for craftsperson/python/colocated-module-specifications.

Pytest `python_files` names the `*_spec.py` convention, every spec module sits
in the package directory of the module it specifies, and no test module lives
in a separate tests directory.

A thin entry point: the check itself lives in ../lib/adherence/checks.py and
the invocation protocol in ../README.md.
"""

import pathlib
import sys

INTENT = "craftsperson/python/colocated-module-specifications"
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
