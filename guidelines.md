# 0 - Project Identity & Context

To be written.

---

# 1 - Universal Engineering Principles

* **Code is communication** — optimise for the next human reader.
* **Simple Design Heuristics** — guiding principles, not iron laws; consult the user when you need to break them.
  1. **All tests pass** — correctness is non‑negotiable.
  2. **Reveals intent** — code should read like an explanation.
  3. **No *****knowledge***** duplication** — avoid multiple spots that must change together; identical code is only a smell when it hides duplicate *decisions*.
  4. **Minimal entities** — remove unnecessary indirection, classes, or parameters.
* **Small, safe increments** — single‑reason commits; avoid speculative work (**YAGNI**).
* **Tests are the executable spec** — red first, green always; test behaviour not implementation.
* **Compose over inherit**; favour pure functions where practical, avoid side-effects.
* **Psychological safety** — review code, not colleagues; critique ideas, not authors.
* **Version‑control etiquette** — descriptive commit messages, branch from `main`, PRs require green CI.

---

# 2 - Python‑Specific Conventions

## 2.1 Runtime & Environment

* **Python ≥ 3.12** (support the two most recent LTS releases).
* Create an isolated environment:

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -e ".[dev]"
  ```
* Enforce `pre‑commit` hooks (flake8, mypy, black, pytest).

## 2.2 Core Libraries

Mandatory: pydantic, structlog, pytest, pytest-spec, pytest-cov, pytest-mock, flake8, black, pre‑commit, mkdocs‑material. Add new libs only when they eliminate **significant** boilerplate or risk.

## 2.3 Project Structure & Imports

* **src‑layout**: code in `src/<package_name>/`; tests live beside code as `*_spec.py`.
* Import order: 1) stdlib, 2) third‑party, 3) first‑party — each group alphabetised with a blank line.

## 2.4 Naming & Style

* `snake_case` for functions & vars, `PascalCase` for classes, `UPPER_SNAKE` for constants.
* Prefix intentionally unused vars/args with `_`.
* **flake8** (with plugins) handles linting, and **black** auto‑formats code. Max line length **100**.
* Cyclomatic complexity cap: **10** (flake8 `C901`).
* Use **f‑strings**; avoid magic numbers.

## 2.5 Type Hints & Docstrings

* **100 % type coverage**; code must pass `mypy --strict`.
* Use `pydantic.BaseModel` for data models; don't use bare `@dataclass` if validation is needed.
* Docstrings in Google format; omit the obvious.

## 2.6 Logging & Observability

* Configure **structlog** for JSON output by default.
* Never use `print` for diagnostics; reserve for user‑facing CLI UX.
* Log levels: `DEBUG` (dev detail) → `INFO` (lifecycle) → `WARNING` (recoverable) → `ERROR` (user visible).

## 2.7 Testing Strategy

* **pytest** with **pytest-spec** for specification-style output.
* Test files end with `_spec.py` and live in the same folder as the code under test.
* Use **Arrange / Act / Assert** blocks separated by a blank line (no comments) **or** BDD `describe/should` classes.
* Function names: use `should_*` and BDD-style specifications.
* Class names: use `Describe*` and BDD-style test suites.
* **Mocking**: Use `pytest-mock`'s `mocker` fixture; don't use `unittest.mock.MagicMock` directly.
* One behavioural expectation per test. Fixtures are helpers, not magic.
* Tests should fail for one reason, avoid multiple assert statements, split the test cases

## 2.8 Dependency & Build Management

* `pyproject.toml` is the **single source of truth**.
* Pin dev deps with sensible upper bounds to avoid surprise breaks.

## 2.9 Release & Versioning

* **Semantic Versioning** `MAJOR.MINOR.PATCH`.
* Maintain a `CHANGELOG.md` using **Added / Changed / Fixed / Removed** sections in the "Keep a Change Log" format.

## 2.10 Documentation Standards

* Build docs with **MkDocs + Material**; auto‑generate API docs via `mkdocstrings`.
* Use Mermaid for diagrams rather than ASCII art.

## 2.11 Example Code

* Runnable snippets live in `src/_examples/`.

---

# 3 - Extending in a Project Layer

1. Append `# Project‑Specific Guidelines` **below** this file when composing the full document.
2. Reference only variations — do **not** repeat common rules.
3. If overriding a rule, state the original, the change, and the rationale.
