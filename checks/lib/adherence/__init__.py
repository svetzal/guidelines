"""Deterministic adherence validators for the intent knowledge base.

Every validator under `checks/<language>/` is a thin entry point into this
package: `runner.main` builds a `Workspace` from the finished code, runs the one
check its intent names from `checks.CHECKS`, and prints the verdict a verifier
(cmv) reads. The traversals the checks share live in `predicates`; the Rust
facts come from the `rustfacts` helper binary.

Standard library only. Nothing here asks a model, reads a transcript, touches
the network, or reads the clock.
"""
