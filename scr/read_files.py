import csv
import os
import json
def read_product_id_csv(path):
    ids = set()

    target_col = 0
    if os.path.exists(path):
        with open(path, mode='r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                ids.add(row[target_col])
    else:
        print(f"Error: File not found at {path}")
        return ids
    return list(ids)

def read_error_ids(path):
    ids = set()
    if os.path.exists(path):
        with open(path, "r") as file:
            content = file.read()
            err_list = content.split("\n")
            for i in err_list:
                ids.add(i.split(" ")[-1])
    else:
        print(f"Error: File not found at {path}")
        return ids
    return list(ids)

def load_checkpoint(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)["last_id"]
    else:
        print(f"Error: File not found at {path}")
    return None