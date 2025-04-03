import os
import json
from pathlib import Path

def find_project_root(target_folder="ml"):
    path = Path(__file__).resolve()
    for parent in path.parents:
        if parent.name == target_folder:
            return parent
    raise RuntimeError(f"Could not find '{target_folder}' in path hierarchy.")

def get_all_absolute(directory: str, exclude: list = []) -> list:
    """
    Scans the specified directory under the project root ('ml') and returns all Python module names,
    excluding __init__.py and non-Python files.

    Args:
        directory (str): Relative path to the module directory (e.g., 'models', 'team_building').
        exclude (list[str]): List of module names (without .py) to exclude.

    Returns:
        List[str]: A list of Python module names (no extensions).
    """
    project_root = find_project_root()
    base_path = project_root / directory

    return [
        f.stem for f in base_path.iterdir()
        if f.suffix == ".py" and not f.name.startswith("__") and f.stem not in exclude
    ]

def get_all(directory, current_file, exclude=[]):
    """
    Scans the specified directory and returns all module names
    (excluding __init__.py and non-Python files).

    Args:
        dir (str): The relative path to the directory.
        current_file (str): Pass in __file__ from the calling test file.

    Returns:
        List[str]: A list of cleaner module names.
    """
    base_path = os.path.join(os.path.dirname(current_file), "..", directory)
    files = os.listdir(base_path)

    return [
        f[:-3] for f in files
        if f.endswith(".py") and not f.startswith("__") and f[:-3] not in exclude
    ]

def load_test_json(filename: str):
    """
    Loads a JSON file from the tests/test_data directory.

    Args:
        filename (str): Name of the JSON file (e.g. 'test_cleaned_data.json')

    Returns:
        dict or list: Parsed JSON content
    """

    if not filename.endswith(".json"):
        filename += ".json"

    test_data_path = Path(__file__).parent.parent / "data" / "test_data"
    with open(test_data_path / filename, "r", encoding="utf-8") as f:
        return json.load(f)