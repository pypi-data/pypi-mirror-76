import json
import numpy as np


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.int32) or isinstance(obj, np.int64):
            return int(obj)


def parse_json_file(file_path: str):
    """utility method to read a json file and return json object

    Parameters
    ----------
    file_path : str
        full path to json file that needs to be parsed

    Returns
    -------
    [type]
        json object parsed from the file
    """
    with open(file_path, "r") as f:
        json_data = json.load(f)

    return json_data


def store_json_data(file_path: str, json_data) -> None:
    """utility method to store data as json to a file with pre-defined
    encoders for numpy objects

    Parameters
    ----------
    file_path : str
        full path to json file where the data needs to be stored
    json_data : [type]
        data that needs to be encoded as json
    """
    with open(file_path, "w") as f:
        json.dump(json_data, f, cls=JsonEncoder)
