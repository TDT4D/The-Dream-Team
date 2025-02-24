from pathlib import Path
import json


"""For loading and saving data (locally)"""

this_dir  = Path(__file__).resolve().parent
data_dir = this_dir.parent/"data"


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
    
    data_file = data_dir/file_name
    with data_file.open("r") as file:
        data = json.load(file)

    return data


def save_json(file_name:str, data:dict) -> bool:
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
    
    data_file = data_dir/file_name

    try:
        with data_file.open("w") as file:
            json.dump(data, file)

        return True
    
    except Exception as e:
        print(f"ERROR: {e}")
        return False


