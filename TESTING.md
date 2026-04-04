# ezdmb Testing Guide

This document describes how to run and write tests for the ezdmb project using pytest.

## Quick Start

### Install pytest

```powershell
pip install pytest
```

### Run all tests

```powershell
cd c:\Users\justi\ezdmb
python -m pytest
```

### Run tests with verbose output

```powershell
python -m pytest -v
```

## Test Organization

Tests are organized alongside source code using the `*_test.py` naming convention:

```text
src/ezdmb/
├── Controller/
│   ├── Configuration.py
│   ├── Configuration_test.py          # Tests for Configuration
│   ├── LoggingUtility.py
│   └── LoggingUtility_test.py          # Tests for LoggingUtility
└── View/
    ├── MenuContentViewUtility.py
    └── MenuContentViewUtility_test.py  # Tests for MenuContentViewUtility
```

## Running Specific Tests

### Run tests for a single file

```powershell
python -m pytest src/ezdmb/Controller/Configuration_test.py -v
```

### Run tests in a specific class

```powershell
python -m pytest src/ezdmb/Controller/Configuration_test.py::TestConfigurationInit -v
```

### Run a specific test function

```powershell
python -m pytest src/ezdmb/Controller/Configuration_test.py::TestConfigurationInit::test_configuration_creates_instance -v
```

### Run tests matching a pattern

```powershell
python -m pytest -k "SaveConfig" -v
```

## Test Fixtures

All test modules use pytest fixtures defined with `@pytest.fixture`:

- **`qapp`**: Creates a QApplication instance needed for PySide6 tests
- **`temp_config_dir`**: Creates a temporary directory for config file tests (auto-cleaned)
- **`mock_config`**: Creates a mock Configuration object for testing views
- **`mock_pixmap_label`**: Creates a mock QLabel for display tests

## Writing Tests

### Test Class Template

```python
class TestMyComponent:
    """Tests for MyComponent functionality"""
    
    def test_feature_does_something(self, qapp, temp_config_dir):
        """Test description of expected behavior"""
        # Arrange
        expected = "value"
        
        # Act
        result = some_function()
        
        # Assert
        assert result == expected
```

### Mocking PySide6 Objects

When testing code that uses PySide6, use `unittest.mock.MagicMock` and `patch`:

```python
from unittest.mock import MagicMock, patch

def test_configuration_signal(self):
    config = MagicMock(spec=Configuration)
    config.configUpdated = MagicMock()
    
    # Use the config
    config.configUpdated.emit({"key": "value"})
    
    # Verify
    config.configUpdated.emit.assert_called_once()
```

## Test Coverage

### Running with coverage (requires pytest-cov)

```powershell
pip install pytest-cov
python -m pytest --cov=src/ezdmb --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`

## Current Test Coverage

| Module | Tests | Status |
|--------|-------|--------|
| Configuration.py | 13 | ✅ 100% |
| LoggingUtility.py | 14 | ✅ 100% |
| MenuContentViewUtility.py | 15 | ✅ 100% |
| **Total** | **42** | ✅ **100%** |

## Common Test Patterns

### Testing file operations

```python
def test_saves_to_file(self, temp_config_dir):
    """Test file writing"""
    config_file = os.path.join(temp_config_dir, 'test.json')
    
    # Your code that writes the file
    write_config(config_file)
    
    # Verify file exists and contains expected data
    assert os.path.exists(config_file)
    with open(config_file, 'r') as f:
        data = json.load(f)
    assert data["key"] == "expected_value"
```

### Testing signal emissions

```python
def test_signal_emitted(self):
    """Test that a signal is properly emitted"""
    config = MagicMock()
    config.configUpdated = MagicMock()
    
    # Code that should emit signal
    trigger_update(config)
    
    # Verify signal was emitted with correct data
    config.configUpdated.emit.assert_called_once()
    args = config.configUpdated.emit.call_args[0]
    assert args[0]["rotate_content"] is True
```

### Testing with temporary files

```python
def test_with_temp_files(self, temp_config_dir):
    """Test code that uses temporary files"""
    test_file = os.path.join(temp_config_dir, 'image.jpg')
    open(test_file, 'a').close()  # Create empty file
    
    # Test code that processes the file
    result = process_image(test_file)
    
    assert result is not None
    # temp_config_dir is auto-cleaned after test
```

## Debugging Tests

### Print debug info

```python
def test_something(self):
    value = compute_value()
    print(f"Debug: computed value = {value}")  # Use print for debugging
    assert value == expected
```

### Run with extra verbosity

```powershell
python -m pytest -vv  # Extra verbose
python -m pytest -s   # Show print statements
```

### Use pytest's `pdb` debugger

```powershell
python -m pytest --pdb  # Drop into debugger on failure
```

## Common Issues

### QApplication already exists

If you get `QApplication already exists`, ensure tests use the `qapp` fixture which manages the application instance.

### Signal not emitted errors

Signals must be properly mocked. Use `MagicMock()` for signal objects and call `.connect()` on mocks.

### Cross-platform file paths

Always use `os.path.join()` for file paths, never hardcode `/` or `\`.

## Adding New Tests

When adding new test files:

1. Follow the naming convention: `ModuleName_test.py`
2. Place in same directory as the module being tested
3. Import the module and required fixtures
4. Organize tests into classes by functionality
5. Use clear, descriptive test names starting with `test_`
6. Add docstrings explaining what is being tested
