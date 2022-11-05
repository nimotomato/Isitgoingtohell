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