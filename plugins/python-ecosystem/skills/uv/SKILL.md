---
name: uv
description: >
  Python project management with uv — the fast, Rust-based package and project manager.
  Use this skill when working in a Python project that has uv.lock, .python-version,
  or when pyproject.toml uses [tool.uv] or [dependency-groups]. Also use when the user
  mentions uv, "uv run", "uv add", or asks about Python dependency management in a
  uv-managed project. Provides project setup, dependency management, running tools,
  and quality gate commands specific to uv workflows.
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---

## uv Project Management

**uv** is the single tool for managing Python versions, virtual environments, dependencies, and running project tools. All project operations go through uv.

### Creating a New Project

```bash
# Create a new project
uv init my-project
cd my-project

# Or initialize in an existing directory
uv init

# Specify a Python version
uv init --python 3.12 my-project
```

This creates: `pyproject.toml`, `.python-version`, `.gitignore`, `README.md`, and a starter `main.py`.

### Managing Python Versions

```bash
# Install specific Python versions
uv python install 3.11 3.12

# Pin the project to a specific version
uv python pin 3.12
```

The pinned version is stored in `.python-version` and used automatically by all uv commands.

### Virtual Environment

uv auto-creates and manages `.venv/` — you rarely need to interact with it directly.

```bash
# Explicitly create a venv (usually automatic)
uv venv

# Sync the environment to match the lockfile
uv sync
```

**Never activate the venv manually.** Use `uv run` to execute everything within the project environment.

### Dependency Management

**Adding dependencies:**
```bash
uv add requests                      # Runtime dependency
uv add 'requests>=2.31,<3'          # With version constraints
uv add git+https://github.com/psf/requests  # From git
uv add -r requirements.txt          # Import from requirements.txt
```

**Adding dev dependencies:**
```bash
uv add --dev pytest                  # Default dev group
uv add --dev pytest-cov
uv add --dev pytest-asyncio
uv add --group lint ruff             # Named group
uv add --group docs mkdocs
```

**Removing and upgrading:**
```bash
uv remove requests                   # Remove a dependency
uv lock --upgrade-package requests   # Upgrade specific package
uv lock --upgrade                    # Re-lock all dependencies
```

### pyproject.toml Structure

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.31,<3",
    "pydantic>=2.0",
]

[project.optional-dependencies]
excel = ["openpyxl>=3.1.0"]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.23",
    {include-group = "lint"},
]
lint = ["ruff>=0.4"]
docs = ["mkdocs>=1.5"]

[tool.uv]
default-groups = ["dev", "lint"]
```

### Lockfile

`uv.lock` is a cross-platform lockfile. Auto-generated, commit to version control.

```bash
uv lock              # Update lockfile from pyproject.toml
uv sync              # Sync environment to lockfile
uv sync --group docs # Sync specific groups
uv sync --no-dev     # Production-only sync
```

### Running Project Tools

**Always use `uv run` for project tools:**
```bash
uv run pytest                    # Run tests
uv run pytest --cov              # Tests with coverage
uv run ruff check src            # Linting
uv run ruff format src           # Formatting
uv run mypy src                  # Type checking
uv run python -m mypackage       # Run application
```

**Use `uvx` for standalone/ephemeral tools:**
```bash
uvx ruff check .                 # One-off tool without installing
uvx ruff@0.4.0 check .           # Specific version
```

**Rule of thumb:** `uv run` when the tool needs your project code. `uvx` for standalone utilities.

### Building

```bash
uv build    # Produces wheel and sdist in dist/
```

### Project Structure

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── conftest.py
│       ├── core/
│       │   ├── pricing.py
│       │   └── pricing_spec.py
│       ├── adapters/
│       │   ├── payment_gateway.py
│       │   └── payment_gateway_spec.py
│       └── cli.py
├── docs/
├── pyproject.toml
├── uv.lock
├── .python-version
└── README.md
```

### Dependency Best Practices

- Use `uv add` / `uv remove` — never edit pyproject.toml by hand for deps
- Use `uv add --dev` for dev-only dependencies
- Use `uv add --group <name>` for named dependency groups
- Version ranges for libraries, pin versions for applications
- Keep `uv.lock` committed for reproducible builds
- Run `uv sync` after cloning or pulling

## Quality Gates (uv)

Before considering any code complete, **MUST** complete all steps:

1. **Tests with Coverage**
   - `uv run pytest` — all tests pass
   - `uv run pytest --cov` — coverage above threshold (**MANDATORY**)
   - Debug: `uv run pytest path/to/test.py -v` or `uv run pytest --lf`

2. **Linting with ZERO warnings**
   - `uv run ruff check src` — zero warnings (**MANDATORY**)
   - `uv run ruff format src` — consistent formatting
   - McCabe complexity <= 10

3. **Security Audit**
   - `uvx pip-audit` — check for known vulnerabilities (**MANDATORY**)
   - `uv pip list --outdated` — check for outdated dependencies

4. **Documentation Sync**
   - `uv run mkdocs build` — verify docs build
   - Ensure examples match current implementation
