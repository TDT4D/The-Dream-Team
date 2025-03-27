import pytest
from data_handling import get_cleaner
from utils.testing_utils import get_all

CLEANER_DIRECTORY = "data_handling"
REQUIRED_FUNCTIONS = ["clean_data"]
EXCLUDE = ["data_cleaning"]

@pytest.mark.parametrize("cleaner_name", get_all(CLEANER_DIRECTORY, __file__, EXCLUDE))
def test_cleaner_has_required_functions(cleaner_name):
    cleaner = get_cleaner(cleaner_name)
    
    for func in REQUIRED_FUNCTIONS:
        assert hasattr(cleaner, func), f"{cleaner_name} is missing function: {func}"
        assert callable(getattr(cleaner, func)), f"{cleaner_name}.{func} is not callable"
