import importlib

def get_cleaner(cleaner_name:str):
    """
    Dynamically loads a cleaner.
    
    Args:
        cleaner_name (str): The name of the cleaner to load (e.g., "data_cleaning_version2").
    
    Returns:
        A cleaner instance from the specified module.
        
    Raises:
        ValueError: If the specified cleaner module does not exist.
    """
    try:
        return importlib.import_module(f"data_handling.{cleaner_name}")
    except ModuleNotFoundError:
        raise ValueError(f"Model '{cleaner_name}' not found")