# Starter‑Kit Generator Prompt

This canvas contains a **re‑usable prompt template** and **baseline file skeletons** for bootstrapping any new Python project that adheres to the *Common Engineering Guidelines*.  Copy the prompt,### 2.11 src/{{package\_name}}/**init**.py

```python
"""{{project_description}}"""
```

---parameters, and run it in ChatGPT (or another LLM) to generate a ready‑to‑commit starter repository.

---

## 1 · Prompt Template

Paste the following into ChatGPT and substitute the values in <angle brackets> (or adjust the JSON block at the top if your tool supports structured input).

````text
You are an assistant that creates fully‑populated starter files for a new Python project.
All output **must** be provided as fenced code‑blocks, one block per file, labelled with the filename as the info‑string (e.g. ```toml pyproject.toml```).

### Parameters
project_name      = <My Cool Project>
package_name      = <coolproj>
project_description = <One‑sentence purpose>
author_name       = <Stacey Vetzal>
author_email      = <me@example.com>
license_type      = <MIT | Apache‑2.0 | Proprietary>
python_version    = 3.12

### Required files to emit
- pyproject.toml (includes Black, flake8, mypy, coverage configs)
- .flake8
- pytest.ini
- .pre-commit-config.yaml
- .gitignore
- README.md (with install + usage)
- LICENSE (matching license_type)
- mkdocs.yml (Material theme)
- docs/index.md (placeholder)
- CHANGELOG.md (keep/unreleased heading)
- src‑layout: code in `src/<package>/`; **tests live beside the modules** as `*_spec.py` (no separate `tests/` directory).

Use the skeletons that follow as defaults; replace placeholders ({{variable}}) with the provided parameters.  Follow the *Common Engineering Guidelines* for all tool settings.
````

---

## 2 · Baseline File Skeletons

Below are terse starting points that align with the guidelines.  When the prompt above runs, each `{{placeholder}}` should be replaced.

### 2.1 pyproject.toml

```toml pyproject.toml
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{{project_name}}"
version = "0.1.0"
description = "{{project_description}}"
readme = "README.md"
license = {text = "{{license_type}}"}
authors = [ { name = "{{author_name}}", email = "{{author_email}}" } ]
requires-python = ">={{python_version}}"

dependencies = [
  "pydantic>=2.7",
  "structlog>=24.1"
]

[project.optional-dependencies]
dev = [
  "black>=24.4",
  "flake8>=7.0",
  "flake8-bugbear>=24.2",
  "flake8-comprehensions>=3.14",
  "flake8-docstrings>=1.7",
  "mypy>=1.10",
  "pytest>=8.3",
  "pytest-spec>=3.2",
  "pytest-mock>=3.12",
  "pytest-cov>=5.0",
  "pre-commit>=3.7",
  "mkdocs-material>=9.5"
]

[tool.black]
line-length = 100
target-version = ["py312"]

[tool.flake8]
max-line-length = 100
extend-select = ["B", "C", "D"] # bugbear, comprehensions, docstrings
ignore = ["E203", "W503"]

[tool.mypy]
python_version = "{{python_version}}"
strict = true

[tool.coverage.run]
branch = true
source = ["{{package_name}}"]
```

### 2.2 .flake8

```ini .flake8
[flake8]
max-line-length = 100
extend-select = B,C,D
ignore = E203,W503
show-source = True
```

### 2.3 pytest.ini

```ini pytest.ini
[pytest]
spec_header_format = {module_path}:
spec_test_format = {result} {name}
spec_ignore = FLAKE8
spec_success_indicator = ✓

# File patterns for test discovery
python_files = test_*.py *_test.py *_spec.py

# Display settings for better specification-style output
addopts =
    --spec
    --tb=short
    --showlocals
    --color=yes
    --cov={{package_name}}

# Custom test summary
testpaths = src

# Improve readability of test names
python_functions = test_* should_*
python_classes = Test* Describe*

# Configure test collection
norecursedirs = .* build dist venv site
```

### 2.4 .pre-commit-config.yaml

```yaml .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black
  - repo: https://gitlab.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
  - repo: https://github.com/pytest-dev/pytest
    rev: 8.2.0
    hooks:
      - id: pytest
```

### 2.5 .gitignore

```gitignore .gitignore
# Bytecode & distribution
__pycache__/
*.py[cod]
*.egg*
dist/
build/

# Virtual envs
.venv/
.env

# Test & coverage reports
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/
.cache/

# Editor folders
.idea/
.vscode/

# OS files
.DS_Store
```

### 2.6 README.md

````markdown README.md
# {{project_name}}

{{project_description}}

## Installation
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
````

## Usage

```python
import {{package_name}}
```

````

### 2.7 LICENSE
```text LICENSE
<Insert {{license_type}} boilerplate here>
````

### 2.8 mkdocs.yml

```yaml mkdocs.yml
site_name: {{project_name}}
site_description: {{project_description}}
theme:
  name: material
plugins:
  - search
  - mkdocstrings
markdown_extensions:
  - admonition
  - codehilite
nav:
  - Home: index.md
```

### 2.9 docs/index.md

```markdown docs/index.md
# Welcome to {{project_name}}

Coming soon.
```

### 2.10 CHANGELOG.md

```markdown CHANGELOG.md
## [Unreleased]
- Initial scaffold.
```

### 2.11 src/{{package\_name}}/**init**.py

```python
"""{{project_description}}"""
```

### 2.12 tests/**init**.py

```python
"""Test package for {{project_name}}."""
```

---

## 3 · Updating This Starter Kit

Keep this canvas in sync with the *Common Engineering Guidelines*; whenever the guidelines change tooling or versions, update the skeletons accordingly so that newly generated projects stay in lock‑step.
