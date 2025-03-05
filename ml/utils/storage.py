from pathlib import Path
import json
import joblib


"""For loading and saving data (locally)"""

this_dir  = Path(__file__).resolve().parent
load_dir = this_dir.parent/"data"   #Directory where to load data
save_dir = this_dir.parent/"data"   #Directory to save data

#Model storage path
model_dir = this_dir.parent/"data"/"saved_models"   #Save/load ml_models
model_dir.mkdir(parents=True, exist_ok=True)

def load_json(file_name:str) -> dict:
    """
    Loads a json file from local storage

    Args:
        file_name (string): name of the json data file

    Returns:
        dict: containing data.

    """

    if not file_name.endswith(".json"):
        file_name += ".json"
    
    data_file = load_dir/file_name

    try:
        with data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    
    except Exception as e:
        print(f"ERROR WHILE LOADING DATA : {e}")
        return []



def save_json(data:dict, file_name:str) -> bool:
    """
    Saves a json file to local storage

    Args:
        file_name (string): name of the json file
        data (dict): data to be saved

    Returns:
        confirmation of the save

    """

    if not file_name.endswith(".json"):
        file_name += ".json"
    
    data_file = save_dir/file_name

    try:
        with data_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

        return True
    
    except Exception as e:
        print(f"ERROR WHILE SAVING DATA: {e}")
        return False

def save_model(model, file_name:str) -> bool:
    """
    Saves a machine learning model to local storage using joblib.

    Args:
        model: The trained model to save.
        file_name (str): The name of the model file.

    Returns:
        bool: Confirmation of the save.
    """

    if not file_name.endswith(".joblib"):
        file_name += ".joblib"
    
    model_file = model_dir / file_name

    try:
        joblib.dump(model, model_file)
        print(f"Model saved to {model_file}")
        return True
    except Exception as e:
        print(f"ERROR WHILE SAVING MODEL: {e}")
        return False


def load_model(file_name:str):
    """
    Loads a machine learning model from local storage using joblib.

    Args:
        file_name (str): The name of the model file.

    Returns:
        The loaded model, or None if loading fails.
    """

    if not file_name.endswith(".joblib"):
        file_name += ".joblib"
    
    model_file = model_dir / file_name

    try:
        model = joblib.load(model_file)
        print(f"Model loaded from {model_file}")
        return model
    except Exception as e:
        print(f"ERROR WHILE LOADING MODEL: {e}")
        return None
