#!/usr/bin/env python3
"""Validator for craftsperson/rust/use-results-for-recoverable-library-errors.

Public fallible functions return Result, and code outside test scope contains
no unwrap, expect, or panicking macro.

A thin entry point: the check itself lives in ../lib/adherence/checks.py and
the invocation protocol in ../README.md.
"""

import pathlib
import sys

INTENT = "craftsperson/rust/use-results-for-recoverable-library-errors"
LANGUAGE = "rust"


def main():
    # Never write bytecode into the knowledge-base tree: a verifier may run
    # this from a scratch copy of a pinned revision.
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "lib"))
    from adherence import runner

    return runner.main(INTENT, LANGUAGE)


if __name__ == "__main__":
    sys.exit(main())
