import importlib

def get_model(model_name:str):
    """
    Dynamically loads a models.
    
    Args:
        model_name (str): The name of the model to load (e.g., "randomforest_v2", "meta_model_v1").
    
    Returns:
        A model instance from the specified module.
        
    Raises:
        ValueError: If the specified model module does not exist.
    """
    try:
        return importlib.import_module(f"models.{model_name}")
    except ModuleNotFoundError:
        raise ValueError(f"Model '{model_name}' not found")