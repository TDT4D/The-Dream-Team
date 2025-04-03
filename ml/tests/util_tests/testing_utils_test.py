"""
Tests for utils/testing_utils.py.

Covers:
- Loading test data JSON files from /ml/data/test_data
- Listing Python module names using both relative and absolute logic
- Excluding specific filenames from module discovery

Functions tested:
- load_test_json()
- get_all(): requires caller to pass a base path
- get_all_absolute(): resolves from the project root (via testing_utils)

Note:
- Validates both JSON parsing and dynamic module listing
- Includes exclusion logic for module filtering
"""


from utils.testing_utils import load_test_json, get_all_absolute, get_all
from pathlib import Path


def test_load_test_json_file_exists():
    data = load_test_json("test_cleaned_data.json")
    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)

def test_load_test_json_file_missing_extension():
    data = load_test_json("test_cleaned_data")  # without .json
    assert isinstance(data, list)
    assert isinstance(data[0], dict)

def test_get_all_absolute_returns_python_modules():
    modules = get_all_absolute("models")
    assert isinstance(modules, list)
    assert all(isinstance(m, str) for m in modules)
    assert all(not m.startswith("__") for m in modules)
    assert all(m.endswith(".py") is False for m in modules)

def test_get_all_returns_python_modules():
    current_file = Path(__file__).resolve().parents[0]
    modules = get_all("models", current_file)
    assert isinstance(modules, list)
    assert all(isinstance(m, str) for m in modules)
    assert all(not m.startswith("__") for m in modules)
    assert all(m.endswith(".py") is False for m in modules)


def test_get_all_excludes_specified_files():
    current_file = Path(__file__).resolve().parents[0]
    modules = get_all("models", current_file, exclude=["random_forest"])
    assert "random_forest" not in modules

    
def test_get_all_absolute_excludes_specified_files():
    modules = get_all_absolute("models", ["random_forest"])
    assert "random_forest" not in modules