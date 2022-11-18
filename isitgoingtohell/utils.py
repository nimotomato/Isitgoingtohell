import toml
import json
import os
from csv import DictReader, DictWriter

def load_csv(file_path):
    with open(file_path, newline='') as f:
        data = list(DictReader(f))
    
    return data

def write_csv(file_path, data: dict):
    with open(file_path, "w", newline='') as outfile:
   
        fieldnames = list(data.keys())
        
        writer = DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row.lower())

        

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
        os.remove(file_path)

