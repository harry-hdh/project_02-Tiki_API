import csv
import os
import json
def read_product_id_csv(path):
    ids = []

    target_col = 0
    if os.path.exists(path):
        with open(path, mode='r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                ids.append(row[target_col])
    return ids[:9999]

def read_error_ids(path):
    ids = []
    if os.path.exists(path):
        with open(path, "r") as file:
            content = file.read()
            err_list = content.split("\n")
            for i in err_list:
                ids.append(i.split(" ")[-1])
    return ids

def load_checkpoint(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)["last_id"]
    return None