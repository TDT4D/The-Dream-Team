import pytest
from models import get_model
from utils.testing_utils import get_all

MODEL_DIRECTORY = "models"
REQUIRED_FUNCTIONS = ["train", "predict"]
EXCLUDE = ["random_forest"]

@pytest.mark.parametrize("model_name", get_all(MODEL_DIRECTORY, __file__, EXCLUDE))
def test_model_has_required_functions(model_name):
    model = get_model(model_name)
    
    for func in REQUIRED_FUNCTIONS:
        assert hasattr(model, func), f"{model_name} is missing function: {func}"
        assert callable(getattr(model, func)), f"{model_name}.{func} is not callable"
