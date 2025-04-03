

def validate_model(model_type:str, model_name:str) -> bool:
    """
    Validates that the model_name matches the expected model_type.
    - ModelName must start with (and include) modelType
    Args:
        model_type (str): The type of the model (e.g., "randomforest_v2").
        model_name (str): The name of the saved model (e.g., "randomforest_v2_test").

    Returns:
        bool: True if valid, False otherwise.
    """
    return model_name.startswith(f"{model_type}")