from pathlib import Path
import json


"""For loading and saving data (locally)"""

this_dir  = Path(__file__).resolve().parent
load_dir = this_dir.parent/"data"   #Directory where to load data
save_dir = this_dir.parent/"data"   #Directory to save data


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


