import importlib

def get_team_builder(team_builder_name:str):
    """
    Dynamically loads a models.
    
    Args:
        get_team_builder (str): The name of the builder to load
    
    Returns:
        A team_builder instance from the specified module.
        
    Raises:
        ValueError: If the specified model module does not exist.
    """
    try:
        return importlib.import_module(f"team_building.{team_builder_name}")
    except ModuleNotFoundError:
        raise ValueError(f"Model '{team_builder_name}' not found")