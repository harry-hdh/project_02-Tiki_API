from read_csv import read_product_id_csv, read_error_ids
from pathlib import Path
from Utilities import *
    
                
def chunked(lst, size):
    for i in range(0,len(lst), size):
        yield lst[i:i + size]


# API endpoints to list
def get_prod_url(pids):
    products_url = []
    for p in pids:
        url = f'https://api.tiki.vn/product-detail/api/v1/products/{p}'
        products_url.append(url)
        # url_pid = (url,p)
    return products_url

# Read pid from csv
product_ids = read_product_id_csv()
#chunk the list to smaller batches low
for i, batch in enumerate(chunked(get_prod_url(product_ids), 1500), 1):
    run_parallel((i, batch))

#Check if error log exists
file_path = Path("./files/error_log.txt")
if file_path.is_file():
    # Retry error products
    err_product_ids = read_error_ids(file_path)
    for i, batch in enumerate(chunked(get_prod_url(err_product_ids), 1500), 1):
        run_parallel((i, batch),'RETRY')


	

