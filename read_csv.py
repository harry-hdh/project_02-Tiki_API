import csv
def read_product_id_csv():
    ids = []

    target_col = 0

    with open('products-0-200000.csv', mode='r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            ids.append(row[target_col])
    return ids[:9999]

def read_error_ids(path):
    ids = []
    with open(path, "r") as file:
        content = file.read()
        err_list = content.split("\n")
        for i in err_list:
            ids.append(i.split(" ")[-1])
