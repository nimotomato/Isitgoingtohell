import toml
import json
import os
from csv import DictReader, DictWriter

def load_csv(file_path):
    with open(file_path, newline='') as f:
        data = list(DictReader(f))
    
    return data

def number_of_keys(data: dict) -> int:
        return len(data[0].keys())

def list_tuple_to_dict(data: list[tuple], keywords: list) -> dict:
    dict_list = []

    for item in data:
        dict_list.append(tuple_to_dict(item, keywords))
        
    return dict_list

def tuple_to_dict(data: tuple, keywords: list) -> dict:
    #WARNING: list of keywords must correspond to items in list.
    x = 0
    new_dict = {}
    while x < len(keywords):
        new_dict[keywords[x]] = data[x]
        x += 1
    return new_dict

def stringify_list(data: list)-> str:
    return ",".join(data)

def fetchall_to_list(fetchall_data: list[tuple]) -> list:
    return [i[0] for i in fetchall_data]

def write_csv(file_path, data: dict):
    with open(file_path, "w", newline='') as outfile:
   
        fieldnames = list(data.keys())
        
        writer = DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row.lower())

def dicts_to_tuples(data):
    # Turn list of dicts into list of tuples
    new_list = []
    for x in data:
        new_list.append(tuple(x.values()))
    return new_list        

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

