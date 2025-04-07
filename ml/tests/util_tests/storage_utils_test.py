"""
Tests for the utils/storage.py module.

Covers:
- Saving and loading JSON files
- Saving and loading ML models using joblib
- Handling of missing or invalid files

Note:
- Uses real test data located in /ml/data/test_data
- Uses a dummy object to test model serialization
"""

from utils import storage
from pathlib import Path

# Setup paths to test data
TEST_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "test_data"
EXISTING_JSON = "test_empty_util_data"  # Without .json extension
NON_EXISTENT_JSON = "non_existent_file"
TEMP_SAVE_FILE = "temp_test_output"

# Dummy model class
class DummyModel:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, DummyModel) and self.name == other.name


def test_load_existing_json():
    data = storage.load_json(EXISTING_JSON)
    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)

def test_load_nonexistent_json():
    result = storage.load_json(NON_EXISTENT_JSON)
    assert result is None

def test_save_json_and_load_back():
    sample_data = {"test": 123, "value": [1, 2, 3]}
    saved = storage.save_json(sample_data, TEMP_SAVE_FILE)
    assert saved is True

    loaded = storage.load_json(TEMP_SAVE_FILE)
    assert loaded == sample_data

    # Clean up
    (storage.save_dir / f"{TEMP_SAVE_FILE}.json").unlink(missing_ok=True)


def test_save_and_load_model():
    model = DummyModel("test_model")
    saved = storage.save_model(model, TEMP_SAVE_FILE)
    assert saved is True

    loaded = storage.load_model(TEMP_SAVE_FILE)
    assert isinstance(loaded, DummyModel)
    assert loaded == model

    # Clean up
    (storage.model_dir / f"{TEMP_SAVE_FILE}.joblib").unlink(missing_ok=True)


def test_load_nonexistent_model():
    model = storage.load_model("non_existent_model_file")
    assert model is None