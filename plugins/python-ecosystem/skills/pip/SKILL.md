---
name: pip
description: >
  Python dependency management with pip and venv. Use this skill when working in a
  Python project that uses pip, requirements.txt, setup.py, or pyproject.toml without
  uv.lock. Also use when the user mentions pip, venv, virtualenv, or asks about Python
  dependency management in a traditional pip-managed project. Provides dependency
  management patterns and quality gate commands for pip workflows.
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---

## Dependency Management with pip

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
└── README.md
```

### Dependencies

- Pin versions in `pyproject.toml` for applications
- Use version ranges for libraries
- Separate dev dependencies via `[project.optional-dependencies]`

## Quality Gates (pip)

Before considering any code complete, **MUST** complete all steps:

1. **Tests with Coverage**
   - `pytest` — all tests pass
   - `pytest --cov` — coverage above threshold (**MANDATORY**)
   - Debug: `pytest path/to/test.py -v` or `pytest --lf`

2. **Linting with ZERO warnings**
   - `ruff check src` — zero warnings (**MANDATORY**)
   - `ruff format src` — consistent formatting
   - McCabe complexity <= 10

3. **Security Audit**
   - `pip-audit` — check for known vulnerabilities (**MANDATORY**)
   - `pip list --outdated` — check for outdated dependencies

4. **Documentation Sync**
   - `mkdocs build` — verify docs build
   - Ensure examples match current implementation
