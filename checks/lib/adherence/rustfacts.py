"""Locate, and on a cache miss build, the `rustfacts` fact extractor.

The Rust checks read facts from a small `syn` binary whose source lives in
`checks/rustfacts/`. Validators must not build it inside the knowledge-base
tree: a verifier may run them from a scratch copy of a pinned revision, where a
`target/` directory is wasted work and pollutes stale detection. So the binary
is found in this order:

1. `RUSTFACTS_BINARY` in the environment;
2. `rustfacts_binary` in the `--config` document (the benchmark passes this);
3. a content-addressed cache, `${XDG_CACHE_HOME:-~/.cache}/guidelines-checks/
   rustfacts/<digest>/release/rustfacts`, where the digest is a SHA-256 over
   `Cargo.toml`, `Cargo.lock`, and every file under `src/`, sorted by path.
   A miss builds with `cargo build --release --locked` into that directory.

Same helper source, same digest, same binary, same facts, wherever the tree was
copied. All cargo output goes to stderr; stdout stays reserved for the verdict.
"""

import hashlib
import os
import pathlib
import subprocess
import sys

CRATE = pathlib.Path(__file__).resolve().parents[2] / "rustfacts"


def locate(config):
    """The extractor binary to run, per the lookup order in the module docs."""
    override = os.environ.get("RUSTFACTS_BINARY")
    if override:
        return pathlib.Path(override)
    configured = config.get("rustfacts_binary")
    if configured:
        return pathlib.Path(configured)
    return cached_binary()


def source_digest(crate=CRATE):
    """SHA-256 over the manifest, lock file, and sources, each prefixed by its path."""
    digest = hashlib.sha256()
    sources = sorted((crate / "src").rglob("*"), key=lambda path: path.as_posix())
    for path in [crate / "Cargo.toml", crate / "Cargo.lock"] + [p for p in sources if p.is_file()]:
        digest.update(path.relative_to(crate).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def cache_root():
    base = os.environ.get("XDG_CACHE_HOME") or pathlib.Path.home() / ".cache"
    return pathlib.Path(base) / "guidelines-checks" / "rustfacts"


def cached_binary(crate=CRATE):
    """The cached binary for the current helper source, building it on a miss."""
    target = cache_root() / source_digest(crate)
    binary = target / "release" / "rustfacts"
    if binary.is_file():
        return binary
    build(crate, target)
    if not binary.is_file():
        raise RuntimeError(f"rustfacts build produced no binary at {binary}")
    return binary


def build(crate, target):
    """Build the extractor into `target`, forwarding cargo's output to stderr.

    The output is forwarded after the build rather than streamed so that, on a
    failure, the first line of stderr is the reason — a verifier reports that
    line — and cargo's own diagnostics follow it.
    """
    target.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [
            "cargo",
            "build",
            "--release",
            "--locked",
            "--manifest-path",
            str(crate / "Cargo.toml"),
            "--target-dir",
            str(target),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        sys.stderr.write(f"rustfacts build failed (cargo exited {completed.returncode})\n")
        sys.stderr.write(completed.stdout)
        raise RuntimeError(f"could not build rustfacts into {target}")
    sys.stderr.write(f"built rustfacts into {target}\n")
    sys.stderr.write(completed.stdout)
