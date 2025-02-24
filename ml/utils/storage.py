from pathlib import Path
import json


"""For loading and saving data (locally)"""

this_dir  = Path(__file__).resolve().parent
data_dir = this_dir.parent/"data"


def load_json(file_name:str) -> dict:
    """
    Loads a json file from locan storage

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

