---
name: pytest-bdd
facet: testing
requires:
  - language/python
scope: "pytest BDD-style specification tests with Describe*/should_* naming, fixture patterns, parametrized tests"
does-not-cover: "Quality gate commands (see quality-gates facets), language idioms (see language/python)"
metadata:
  version: "1.0.0"
  author: Stacey Vetzal
---

## Testing Patterns

**pytest configuration** (in `pyproject.toml`):
```toml
[tool.pytest.ini_options]
python_files = ["*_spec.py"]
python_classes = ["Describe*"]
python_functions = ["should_*"]
```

**Test Organization:**
- One spec file per module, co-located: `module_spec.py` beside `module.py`
- Use `conftest.py` for shared fixtures (place at appropriate package level)
- Separate unit tests (fast, isolated) from integration tests via pytest markers

**BDD-Style Specification Tests:**
- Test classes use `Describe*` prefix, test methods use `should_*` prefix
- Nested `Describe` classes group related behaviors
- Follow Arrange/Act/Assert with blank line separators — never use `# Arrange`, `# Act`, `# Assert` comments
- Use `Mock(spec=ClassName)` for type-safe mocks at gateway boundaries

```python
class DescribeMyComponent:
    @pytest.fixture
    def mock_gateway(self):
        return Mock(spec=SomeGateway)

    @pytest.fixture
    def component(self, mock_gateway):
        return MyComponent(mock_gateway)

    class DescribeSomeMethod:
        def should_return_expected_result(self, component, mock_gateway):
            mock_gateway.fetch.return_value = "data"

            result = component.some_method("input")

            assert result == "expected"
```

**Fixture Patterns:**
```python
@pytest.fixture
def user_factory():
    """Factory fixture for creating test users."""
    def _create_user(**kwargs):
        defaults = {"name": "Test User", "email": "test@example.com"}
        return User(**(defaults | kwargs))
    return _create_user

@pytest.fixture
def mock_database():
    """Mock database gateway at boundary."""
    return Mock(spec=DatabaseGateway)
```

**Parametrized Tests:**
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected
```
