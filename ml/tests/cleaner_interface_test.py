import os
import pytest
from data_handling import get_cleaner

CLEANER_DIRECTORY = "data_handling"
REQUIRED_FUNCTIONS = ["clean_data"]

def get_all_cleaners():
    base_path = os.path.join(os.path.dirname(__file__), "..", CLEANER_DIRECTORY)
    files = os.listdir(base_path)

    cleaners = []
    for file in files:
        if file.endswith(".py") and not file.startswith("__"):
            name = file[:-3]
            cleaners.append(name)
    return cleaners

@pytest.mark.parametrize("cleaner_name", get_all_cleaners())
def test_cleaner_has_required_functions(cleaner_name):
    cleaner = get_cleaner("data_cleaning_version3")
    
    for func in REQUIRED_FUNCTIONS:
        assert hasattr(cleaner, func), f"Missing function: {func}"
        assert callable(getattr(cleaner, func)), f"{func} is not callable"
