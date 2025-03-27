import os

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
