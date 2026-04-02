import csv
def read_product_id_csv():
    ids = []

    target_col = 0

    with open('products-0-200000.csv', mode='r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            ids.append(row[target_col])
    return ids
