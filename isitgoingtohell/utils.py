import toml
import json
import os

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

def delete_local_file(file_path):
        print("Cleanup initiated...")
        # Verify that the file exists.
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} deleted. ")

        print(f"{file_path} does not exist. ")
