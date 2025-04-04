import pytest
from team_building import get_team_builder
from utils.testing_utils import get_all

MODEL_DIRECTORY = "team_building"
REQUIRED_FUNCTIONS = ["build_team"]
EXCLUDE = []

@pytest.mark.parametrize("builder_name", get_all(MODEL_DIRECTORY, __file__, EXCLUDE))
def test_team_builder_has_required_functions(builder_name):
    builder = get_team_builder(builder_name)
    
    for func in REQUIRED_FUNCTIONS:
        assert hasattr(builder, func), f"{builder_name} is missing function: {func}"
        assert callable(getattr(builder, func)), f"{builder_name}.{func} is not callable"
