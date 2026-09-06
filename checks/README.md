# Validators

Codified validators for intent records. An intent record may declare, as an
evidence entry, an executable that decides from source alone whether a project
holds the intent. The verifier — `cmv`, in the
[context-mixer](https://github.com/svetzal/context-mixer2) repository, whose
`CMV.md` is the authoritative protocol — runs them. Nothing here asks a model,
reads an agent transcript, touches the network, or reads the clock, so a verdict
is reproducible wherever the code and this tree are copied.

## Layout

```
checks/
  README.md              this file
  calibrate.py           the calibration gate (see below)
  lib/adherence/         one plain Python package, standard library only (3.11+)
    predicates.py        the traversals checks share: symbol use, containment,
                         construct shape, declared tool config
    checks.py            one check per intent, and the CHECKS map from intent
                         key to check
    workspace.py         a finished workspace partitioned into production and
                         test modules
    runner.py            the shared entry: parse the protocol arguments, run one
                         check, print one verdict
    rustfacts.py         locating (and on a miss, building) the Rust fact
                         extractor
  rust/<slug>.py         one executable entry point per Rust validator
  rustfacts/             the syn-based fact extractor, a standalone crate
  fixtures/<language>/<set>/
    expected.json        per-validator expected verdicts and the config the
                         validators receive
    <arm>/               a workspace fixture, e.g. pass/ and fail/
```

Each entry point is a few lines: it puts `lib/` on `sys.path` and calls
`runner.main(<intent key>, <language>)`. The slug matches the record file name,
so `checks/rust/put-gateways-at-effect-boundaries.py` validates
`intents/craftsperson/rust/put-gateways-at-effect-boundaries.toml`.

## Declaring a validator on a record

```toml
evidence = [
  { type = "architecture_review", description = "...", required = true },
  { type = "static-check", language = "rust", run = "checks/rust/put-gateways-at-effect-boundaries.py", description = "A project-owned gateway trait is declared, implemented by a concrete adapter, and depended upon by at least one module that performs no I/O.", required = true },
]
```

`run` is relative to the repository root. `language` is the source language the
validator reads; the verifier runs the entries matching the languages it detects
in the project. `description` is what an agent sees — cmf renders it into the
guidance — so write it as the observable expectation the check enforces, not as
"runs a script". `required` decides whether a failing verdict fails the
verification run.

## Invocation protocol

The verifier runs each validator as a subprocess, from the repository root:

```text
<repository-root>/checks/<language>/<slug>.py --workspace <project-root> --config <json-file>
```

`--config` names a JSON file holding the intent's block from the project's
`cmv.toml` (an empty object when there is none). The validator writes exactly
one JSON document to stdout and exits 0:

```json
{
  "applicable": true,
  "followed": false,
  "signals": { "declared_traits": {}, "effectful_modules": ["src/http.rs"] },
  "evidence": ["no gateway trait is declared"],
  "locations": [{ "path": "src/http.rs", "line": 14 }]
}
```

- `applicable` — whether the condition the intent governs arose at all. A
  conditional intent whose condition never arose is *not applicable*, never a
  failure, and leaves the adherence denominator.
- `followed` — whether the code holds the intent, when applicable.
- `signals` — the raw facts behind the verdict, so a false verdict shows what
  was and was not found.
- `evidence` — short human-readable observations.
- `locations` — where the observations were made, as workspace-relative paths
  with an optional one-based line, so the verifier can render `path:line`
  diagnostics the way a linter does. A check with no natural location leaves
  it empty.

Anything else — the fact extractor cannot be built, the workspace is
unreadable, the config lacks a key the check needs — is a nonzero exit with the
reason as the first line of stderr. The verifier records that intent as
*unchecked*. A validator never prints a verdict it did not compute, and
everything diagnostic goes to stderr; stdout is the verdict alone.

Config keys the current checks read: `business_rule_pattern` and
`business_rule_minimum_matches` (which literals mark a project's business rules,
for the functional-core check), `package` (the project's package name). Two
more are harness affordances: `rustfacts_binary` (see below) and
`baseline_root`, a workspace whose public items are subtracted so only new work
is scored — the benchmark passes the untouched scenario skeleton. Both do
nothing when absent.

## The `rustfacts` helper binary

Python's `ast` does not read Rust, so the Rust checks take their facts — item
shapes, call sites, macro invocations, and the test scope each sits in — from
`rustfacts/`, a small `syn` binary that emits them as JSON. It carries no
judgement; every verdict is in `checks.py`.

Validators must not build inside this tree. The verifier may run them from a
scratch copy of a pinned revision, where a `target/` directory is wasted work
and pollutes stale detection. `lib/adherence/rustfacts.py` finds the binary in
this order:

1. `RUSTFACTS_BINARY` in the environment;
2. `rustfacts_binary` in the `--config` document (the benchmark passes this);
3. a content-addressed cache,
   `${XDG_CACHE_HOME:-~/.cache}/guidelines-checks/rustfacts/<digest>/release/rustfacts`,
   where `<digest>` is a SHA-256 over `Cargo.toml`, `Cargo.lock`, and every
   file under `src/`, sorted by path. On a miss it runs
   `cargo build --release --locked --manifest-path checks/rustfacts/Cargo.toml --target-dir <that directory>`
   with all cargo output on stderr.

Same helper source, same digest, same binary, same facts, wherever the tree was
copied. A change to the helper's source changes the digest and triggers one
rebuild. `--locked` means a `Cargo.toml` edit must land with its `Cargo.lock`.

## Calibration

A validator that cannot fail measures nothing. Every validator ships with at
least one workspace fixture it is expected to pass and one it is expected to
not pass (fail, or not applicable), in the language it validates, under
`fixtures/<language>/<set>/`. The set's `expected.json` names, per validator
slug and per fixture arm, the verdict fields that must hold, plus the
`check_config` the validators receive:

```json
{
  "check_config": { "business_rule_pattern": "...", "package": "ratecard" },
  "validators": {
    "prefer-fakes-at-boundaries": {
      "pass": { "applicable": true, "followed": true },
      "fail": { "applicable": false }
    }
  }
}
```

The gate:

```bash
python3 checks/calibrate.py
```

runs every validator over every fixture arm through the same argv the verifier
uses, asserts the expected verdict, runs each twice and requires byte-identical
stdout, prints a table, and exits nonzero on any mismatch. It also fails a
validator that has no fixtures or whose fixtures never expect both a pass and a
non-pass. A validator change is not done until calibration is green.

The first Rust fixtures, `fixtures/rust/rate-card/`, are the reference solution
(`pass/`, 8 of 8 followed) and the untouched skeleton (`fail/`, 0 of 7 followed,
`prefer-fakes-at-boundaries` not applicable) of the context-mixer benchmark's
rate-card exercise.

## Adding a validator

1. Write the check in `lib/adherence/checks.py` as `check_<name>(workspace,
   config)` returning `result(...)` or `not_applicable(...)`, and map the intent
   key to it in `CHECKS`. Anything that would have to change per project belongs
   in `config`, not in the check.
2. Add `<language>/<slug>.py` from an existing entry point, `chmod +x`.
3. Add the `static-check` evidence entry to the intent record.
4. Add or extend a fixture set so the validator has a passing and a non-passing
   arm, and record both in `expected.json`.
5. `python3 checks/calibrate.py` until green.
