#!/usr/bin/env python3
"""Read-only configuration and source-candidate checks for Product Atlas."""

import argparse
import codecs
import json
import os
from pathlib import Path
import sys


KINDS = {"code", "documentation", "analytics", "feedback", "runtime", "marketing"}
STORES = {"intent", "questions", "generation", "wiki"}
SKIP = {
    ".git", ".hg", ".svn", ".venv", "venv", "node_modules", "__pycache__",
    "archive", "vendor", "target", "build", "dist", ".next", ".cache",
}
SKIP_FILES = {".DS_Store", "package-lock.json", "yarn.lock", "Cargo.lock", "uv.lock"}
TEMP_PREFIXES = (".product-atlas-stage-", ".product-atlas-backup-")


def inside(path, parent):
    return path == parent or parent in path.parents


def resolve_path(value, base):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Paths must be nonempty strings.")
    path = Path(value).expanduser()
    return (base / path).resolve()


def source_candidate(path):
    """Recognize text and common documents; the agent must read their content."""
    if path.is_symlink() or not path.is_file() or path.name in SKIP_FILES:
        return False
    if path.name == ".env" or path.name.startswith(".env."):
        return False
    if path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
        return False
    try:
        with path.open("rb") as stream:
            sample = stream.read(8192)
        if path.suffix.lower() == ".pdf" and sample.startswith(b"%PDF-"):
            return True
        if path.suffix.lower() in {".docx", ".pptx", ".odt"} and sample.startswith(b"PK\x03\x04"):
            return True
        # A sample can end partway through a multibyte character.
        decoder = codecs.getincrementaldecoder("utf-8")()
        return b"\0" not in sample and bool(decoder.decode(sample, final=False).strip())
    except (OSError, UnicodeError):
        return False


def discover(root, settings, stores):
    def excluded(path):
        resolved = path.resolve()
        return resolved == settings or any(inside(resolved, store) for store in stores)

    if root.is_file():
        return [root] if not excluded(root) and source_candidate(root) else []
    found = []
    def unreadable(error):
        raise ValueError("Cannot read source directory: {}".format(error.filename))
    for directory, folders, files in os.walk(root, followlinks=False, onerror=unreadable):
        current = Path(directory)
        folders[:] = sorted(
            name for name in folders
            if name not in SKIP
            and not name.startswith(TEMP_PREFIXES)
            and not (current / name).is_symlink()
            and not excluded(current / name)
        )
        found.extend(
            current / name for name in sorted(files)
            if not excluded(current / name) and source_candidate(current / name)
        )
    return found


def preflight(settings):
    settings = Path(settings).resolve()
    with settings.open(encoding="utf-8") as stream:
        config = json.load(stream)
    if not isinstance(config, dict) or type(config.get("schema_version")) is not int or config["schema_version"] != 1:
        raise ValueError("Expected a settings object with schema_version 1.")
    if not isinstance(config.get("product"), str) or not config["product"].strip():
        raise ValueError("Set a nonempty product name.")
    paths = config.get("paths")
    if not isinstance(paths, dict) or set(paths) != STORES:
        raise ValueError("paths must define exactly intent, questions, generation, and wiki.")
    stores = {name: resolve_path(value, settings.parent) for name, value in paths.items()}
    for name, path in stores.items():
        if path.exists() and not path.is_dir():
            raise ValueError("{} must be a directory: {}".format(name, path))
        if inside(settings, path):
            raise ValueError("{} would contain the settings file.".format(name))
        if (path / ".git").exists():
            raise ValueError("{} is a Git checkout; choose a dedicated subdirectory.".format(name))
        for other, other_path in stores.items():
            if name != other and inside(path, other_path):
                raise ValueError("Storage paths overlap: {} and {}.".format(name, other))
    sources = config.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("No corpus configured. Supply code or documentation sources.")
    source_ids = set()
    result = []
    warnings = []
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("Each source must be an object with id, kind, and path.")
        source_id, kind = source.get("id"), source.get("kind")
        if not isinstance(source_id, str) or not source_id.strip() or source_id in source_ids:
            raise ValueError("Source IDs must be nonempty and unique.")
        if not isinstance(kind, str) or kind not in KINDS:
            raise ValueError("Unsupported source kind for {}.".format(source_id))
        source_ids.add(source_id)
        root = resolve_path(source.get("path"), settings.parent)
        if any(inside(root, path) for path in stores.values()):
            raise ValueError("Source {} is inside generated output or a registry.".format(source_id))
        if root == settings:
            raise ValueError("The settings file is not a corpus.")
        if not root.exists():
            raise ValueError("Source {} does not exist: {}".format(source_id, root))
        if not root.is_file() and not root.is_dir():
            raise ValueError("Source {} must be a regular file or directory.".format(source_id))
        files = discover(root, settings, stores.values())
        if not files:
            warnings.append("{} has no source candidates. Export unsupported binary formats to text if needed.".format(source_id))
        result.append({"id": source_id, "kind": kind, "path": str(root), "files": [str(p) for p in files]})
    if not any(source["files"] and source["kind"] in {"code", "documentation"} for source in result):
        raise ValueError("No readable code or documentation corpus. Supply material to digest; registries and generated output do not qualify.")
    return {
        "status": "candidates-found",
        "settings": str(settings),
        "product": config["product"],
        "paths": {name: str(path) for name, path in stores.items()},
        "sources": result,
        "excluded_directory_names": sorted(SKIP),
        "excluded_directory_prefixes": list(TEMP_PREFIXES),
        "warnings": warnings,
        "next": "Read the candidates. Decline if they contain no useful product material. This check does not establish semantic sufficiency.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", default=".product-atlas.json", help="Project settings JSON path")
    args = parser.parse_args()
    try:
        result = preflight(args.settings)
    except (OSError, ValueError, RuntimeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
