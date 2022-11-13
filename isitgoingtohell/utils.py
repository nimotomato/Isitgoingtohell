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

def write_json(dictionary, file_path='result.json'):
    # Write json-formatted data to file.
    json_object = json.dumps(dictionary, indent=1)

    with open(file_path, "w") as f:
        f.write(json_object)

def delete_local_file(file_path):
        print("Cleanup initiated...")
        # Verify that the file exists.
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} deleted. ")
        else:
            print(f"{file_path} does not exist. ")
