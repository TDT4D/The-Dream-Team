import pytest
from models import get_model
from utils.testing_utils import get_all
from pathlib import Path

this_dir = Path(__file__).resolve().parent
test_file = str(this_dir.parent / "data" / "cleaned_data_test.json")

MODEL_DIRECTORY = "models"
REQUIRED_FUNCTIONS = ["train", "predict"]
EXCLUDE = ["random_forest"]


@pytest.mark.parametrize("model_name", get_all(MODEL_DIRECTORY, __file__, EXCLUDE))
def test_model_has_required_functions(model_name):
    model = get_model(model_name)

    for func in REQUIRED_FUNCTIONS:
        assert hasattr(model, func), f"{model_name} is missing function: {func}"
        assert callable(getattr(model, func)), f"{model_name}.{func} is not callable"


@pytest.mark.parametrize("model_name", get_all(MODEL_DIRECTORY, __file__, EXCLUDE))
def test_train(model_name):
    model = get_model(model_name)
    result = model.train(load=test_file, cleaning=False)
    assert result is True, "Training should return True if successful"


@pytest.mark.parametrize("model_name", get_all(MODEL_DIRECTORY, __file__, EXCLUDE))
def test_train_no_data(model_name):
    model = get_model(model_name)
    result = model.train(load="non_existent_file")
    assert result is None, "Training should return None if data file is missing"


@pytest.mark.parametrize("model_name", get_all(MODEL_DIRECTORY, __file__, EXCLUDE))
def test_predict_no_data(model_name):
    model = get_model(model_name)
    result = model.predict(load="non_existent_file", cleaning=True)
    assert result is None, "Predict should return None if data file is missing"


@pytest.mark.parametrize("model_name", get_all(MODEL_DIRECTORY, __file__, EXCLUDE))
def test_predict_no_model(model_name):
    model = get_model(model_name)
    result = model.predict(load=test_file, model_name="non_existing_model", cleaning=False)
    assert result is None, "Predict should return None if model is missing"


@pytest.mark.parametrize("model_name", get_all(MODEL_DIRECTORY, __file__, EXCLUDE))
def test_predict(model_name):
    model = get_model(model_name)
    result = model.predict(load=test_file, cleaning=False)
    # Check that result is list of dicts
    assert isinstance(result, list), "Predict should return a list"
    assert all(isinstance(entry, dict) for entry in result), "All entries should be dictionaries"

    # Assure that results have all necessary data
    required_keys = {"projectId", "studentId", "Predicted_Relation", "Score"}
    assert all(required_keys.issubset(entry.keys()) for entry in result), "Each result must contain required keys"

    # Check, that "projectId", "studentId" and "Score" are Floats
    assert all(isinstance(entry["projectId"], float) for entry in result), "'projectId' should be a float"
    assert all(isinstance(entry["studentId"], float) for entry in result), "'studentId' should be a float"
    assert all(isinstance(entry["Score"], float) for entry in result), "'Score' should be a float"

    # Check, that "Predicted_Relation" is Int
    assert all(
        isinstance(entry["Predicted_Relation"], int) for entry in result), "'Predicted_Relation' should be an int"


@pytest.mark.parametrize("model_name", get_all(MODEL_DIRECTORY, __file__, EXCLUDE))
def test_t_predict_no_data(model_name):
    model = get_model(model_name)
    result = model.t_predict(data="non_existing_file", cleaning=True)
    assert result is None, "t_predict should return None if data file is missing"