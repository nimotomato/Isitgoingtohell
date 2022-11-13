import toml
import json


def load_toml(file_path) -> dict:
    with open(file_path, "r") as f:
        data = toml.load(f)

    return data

def load_json(file_path) -> dict:
    with open(file_path, "r") as f:
        data = json.load(f)

    return data

def write_json(dictionary, filename='result.json'):
    json_object = json.dumps(dictionary, indent=1)

    with open(filename, "w") as outfile:
        outfile.write(json_object)