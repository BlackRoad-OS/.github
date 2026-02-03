# Testing Guide

> **Comprehensive testing infrastructure for BlackRoad prototypes**

---

## Quick Start

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run specific test file
pytest tests/operator/test_parser.py

# Run with coverage
pytest --cov=prototypes --cov-report=html

# Run tests for specific marker
pytest -m unit
pytest -m operator
```

---

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── operator/                # Operator prototype tests
│   ├── __init__.py
│   ├── test_parser.py      # Parser tests (23 tests)
│   ├── test_classifier.py  # Classifier tests (24 tests)
│   └── test_router.py      # Router tests (26 tests)
├── metrics/                 # Metrics prototype tests (TODO)
├── dispatcher/              # Dispatcher prototype tests (TODO)
├── mcp-server/             # MCP server tests (TODO)
└── webhooks/               # Webhook tests (TODO)
```

---

## Test Categories

### Markers

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Fast unit tests, no external dependencies
- `@pytest.mark.integration` - Integration tests with external services
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.operator` - Operator prototype tests
- `@pytest.mark.metrics` - Metrics prototype tests
- `@pytest.mark.dispatcher` - Dispatcher prototype tests

### Running Specific Tests

```bash
# Only unit tests (fast)
pytest -m unit

# Skip slow tests
pytest -m "not slow"

# Only operator tests
pytest -m operator

# Specific test class
pytest tests/operator/test_parser.py::TestParser

# Specific test method
pytest tests/operator/test_parser.py::TestParser::test_parse_simple_text
```

---

## Coverage

### Generating Coverage Reports

```bash
# Terminal report
pytest --cov=prototypes --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=prototypes --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
pytest --cov=prototypes --cov-report=xml
```

### Current Coverage

| Module | Coverage |
|--------|----------|
| Operator Parser | 95% |
| Operator Classifier | 98% |
| Operator Router | 69% |
| **Overall Operator** | **75%** |

---

## Writing Tests

### Test Structure

```python
"""
Tests for the Module Name.

Brief description of what's being tested.
"""

import pytest
from prototypes.module import ClassToTest


class TestClassName:
    """Test suite for ClassName."""
    
    @pytest.fixture
    def instance(self):
        """Create an instance for testing."""
        return ClassToTest()
    
    @pytest.mark.unit
    @pytest.mark.module_name
    def test_basic_functionality(self, instance):
        """Test basic functionality."""
        result = instance.method("input")
        
        assert result == "expected"
        assert isinstance(result, str)
```

### Test Naming

- Test files: `test_*.py` or `*_test.py`
- Test classes: `Test*`
- Test methods: `test_*`
- Use descriptive names: `test_parse_simple_text` not `test1`

### Assertions

```python
# Basic assertions
assert result == expected
assert result is not None
assert isinstance(result, ExpectedType)

# Numeric comparisons
assert value > 0
assert 0 <= confidence <= 1

# String checks
assert "substring" in result
assert result.startswith("prefix")

# Collection checks
assert item in collection
assert len(collection) == 3

# Exception testing
with pytest.raises(ValueError):
    function_that_should_raise()
```

---

## Fixtures

### Shared Fixtures (conftest.py)

```python
@pytest.fixture
def sample_queries():
    """Common test queries."""
    return {
        "ai": ["What is AI?", "Generate code"],
        "crm": ["Sync Salesforce", "Update customer"],
    }

@pytest.fixture
def sample_org_codes():
    """Valid organization codes."""
    return ["OS", "AI", "CLD", "HW", "SEC", ...]
```

### Using Fixtures

```python
def test_with_fixture(sample_queries):
    """Test using a fixture."""
    ai_queries = sample_queries["ai"]
    assert len(ai_queries) > 0
```

### Fixture Scope

```python
@pytest.fixture(scope="module")  # Runs once per module
def expensive_resource():
    return create_resource()

@pytest.fixture(scope="function")  # Runs for each test (default)
def fresh_instance():
    return MyClass()
```

---

## Mocking

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch

def test_with_mock(monkeypatch):
    """Test with mocked dependency."""
    mock_api = Mock(return_value="mocked response")
    monkeypatch.setattr('module.api_call', mock_api)
    
    result = function_that_calls_api()
    
    assert result == "mocked response"
    mock_api.assert_called_once()
```

### Mocking Time

```python
def test_with_fixed_time(mock_datetime):
    """Test with fixed timestamp."""
    # mock_datetime fixture provides fixed time
    result = function_that_uses_datetime()
    assert result.timestamp == "2026-01-27T19:00:00Z"
```

---

## Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_function()
    assert result is not None
```

---

## Parameterized Tests

### Multiple Test Cases

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    """Test uppercase conversion."""
    assert input.upper() == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("query,org_code", [
    ("What is AI?", "AI"),
    ("Deploy worker", "CLD"),
    ("Sync Salesforce", "FND"),
])
def test_routing(query, org_code, operator):
    """Test routing various queries."""
    result = operator.route(query)
    assert result.org_code == org_code
```

---

## Test Organization

### Test Classes

Group related tests in classes:

```python
class TestParser:
    """Tests for Parser class."""
    
    def test_parse_text(self):
        """Test text parsing."""
        pass
    
    def test_parse_http(self):
        """Test HTTP parsing."""
        pass


class TestClassifier:
    """Tests for Classifier class."""
    
    def test_classify_ai(self):
        """Test AI classification."""
        pass
```

### Test Modules

Organize tests by feature:

- `test_parser.py` - Input parsing tests
- `test_classifier.py` - Classification tests
- `test_router.py` - Routing tests

---

## CI/CD Integration

### GitHub Actions

Tests run automatically on:
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`
- Changes to `prototypes/`, `tests/`, or test config files

### Workflow

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements-test.txt
      - run: pytest
```

---

## Best Practices

### Do's ✅

- **Write tests first** (TDD when possible)
- **Test one thing per test** - Keep tests focused
- **Use descriptive names** - `test_parse_empty_string` not `test1`
- **Test edge cases** - Empty strings, None, very long inputs
- **Use fixtures** - Share setup code across tests
- **Mock external dependencies** - Don't hit real APIs in tests
- **Check coverage** - Aim for >80% coverage
- **Keep tests fast** - Unit tests should run in milliseconds

### Don'ts ❌

- **Don't test implementation details** - Test behavior, not internals
- **Don't write brittle tests** - Avoid hardcoded timestamps, random values
- **Don't skip test failures** - Fix them or remove the test
- **Don't test third-party code** - Trust that pytest works
- **Don't duplicate tests** - Use parametrize for similar cases
- **Don't commit .pytest_cache** - Add to .gitignore

---

## Debugging Tests

### Verbose Output

```bash
# Show all test names
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run last failed tests
pytest --lf
```

### Debugging with pdb

```python
def test_something():
    """Test with debugger."""
    result = function()
    import pdb; pdb.set_trace()  # Breakpoint
    assert result == expected
```

Or use pytest's built-in:

```bash
# Drop into pdb on failure
pytest --pdb

# Drop into pdb on error
pytest --pdbcls=IPython.terminal.debugger:Pdb
```

---

## Common Issues

### Import Errors

```bash
# Make sure you're in the repo root
cd /path/to/.github

# Run pytest from root
pytest tests/

# Or use Python module syntax
python -m pytest tests/
```

### Missing Dependencies

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Or install specific package
pip install pytest pytest-cov
```

### Coverage Not Working

```bash
# Make sure coverage is installed
pip install pytest-cov

# Use --cov flag
pytest --cov=prototypes

# Check pytest.ini configuration
cat pytest.ini
```

---

## Test Commands Reference

```bash
# Basic
pytest                              # Run all tests
pytest tests/operator/              # Run operator tests
pytest -v                          # Verbose output
pytest -x                          # Stop on first failure

# Markers
pytest -m unit                     # Only unit tests
pytest -m "not slow"               # Skip slow tests
pytest -m "operator and unit"      # Multiple markers

# Coverage
pytest --cov                       # Basic coverage
pytest --cov=prototypes --cov-report=html  # HTML report
pytest --cov --cov-branch          # Branch coverage

# Output
pytest -s                          # Show print statements
pytest --tb=short                  # Short traceback
pytest --tb=line                   # One-line traceback
pytest -ra                         # Show all test summary

# Selection
pytest tests/operator/test_parser.py                    # Single file
pytest tests/operator/test_parser.py::TestParser       # Single class
pytest tests/operator/test_parser.py::TestParser::test_parse_text  # Single test

# Debugging
pytest --pdb                       # Drop into pdb on failure
pytest --lf                        # Run last failed
pytest --ff                        # Run failed first

# Performance
pytest --durations=10              # Show 10 slowest tests
pytest --benchmark                 # Run benchmarks
```

---

## Resources

- **Pytest Docs:** https://docs.pytest.org/
- **Coverage.py Docs:** https://coverage.readthedocs.io/
- **Testing Best Practices:** https://docs.python-guide.org/writing/tests/

---

*Testing is caring. Write tests. Ship with confidence.* 🧪

📡 **Signal:** `tests → bridge : documented`
