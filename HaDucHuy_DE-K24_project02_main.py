import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import json
import re
from read_csv import read_product_id_csv
from writer import *
from concurrent.futures import ThreadPoolExecutor, as_completed

session = requests.Session()
retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))
		
def extract_api_response(url, batch_num):
    # response = requests.get(url, headers='')
    pid = url.split("/")[-1]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = session.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            
            # This creates a list of all base_urls
            images_list = data.get("images", [])
            
            filtered = {
                "id": data.get("id"),
                "name": data.get("name"),
                "price": data.get("price"),
                "url_key": data.get("url_key"),
                "description": re.sub(r"<.*?>|\n|\r", "", data.get("description")).strip(),
                "image_urls": [img.get("base_url") for img in images_list if img.get("base_url")] if images_list else []
            }

            response_writer(filtered, pid, batch_num)
        else:
            err_writer(f'Status - {response.status_code}', pid)
            
    except Exception as e:
        err_writer(e, pid, response.status_code)
        # print(f"Request failed with status code: {response.status_code}")
        

def run_parallel(url_list_batch, max_workers=20): #Increase max_workers for faster
    batch_num, batch = url_list_batch
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(extract_api_response, item, batch_num) for item in batch]
        for future in as_completed(futures):
            try:
                future.result()  # just to catch exceptions
            except Exception as e:
                print(f"Task failed: {e}")
    
                
def chunked(lst, size):
    for i in range(0,len(lst), size):
        yield lst[i:i + size]


# Read pid from csv
product_ids = read_product_id_csv()

# API endpoints to list
products_url = []
for p in product_ids:
    url = f'https://api.tiki.vn/product-detail/api/v1/products/{p}'
    products_url.append(url)
    # url_pid = (url,p)
    
#chunk the list to smaller batches low
for i, batch in enumerate(chunked(products_url, 1500), 1):
    run_parallel((i, batch))



	

