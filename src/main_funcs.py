from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import re
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from src.write_files import *

session = requests.Session()
retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))
session.mount('http://', HTTPAdapter(max_retries=retries))

def extract_api_response(url, batch_num, file_type=''):
    # response = requests.get(url, headers='')

    pid = url.split("/")[-1]

    header = ''#{'User-Agent': 'Mozilla/5.0'}

    #response = None

    try:
        response = session.get(url, headers=header, timeout=20)
        if response.status_code == 200:
            data = response.json()

            # This creates a list of all base_urls
            images_list = data.get("images", [])

            filtered = {
                "id": data.get("id"),
                "name": data.get("name"),
                "price": data.get("price"),
                "url_key": data.get("url_key"),
                "description": re.sub(r"<.*?>|\n|\r", "", data.get("description") or "").strip(),
                "image_urls": [img.get("base_url") for img in images_list if img.get("base_url")] if images_list else []
            }

            # response_writer(filtered, pid, batch_num, file_type)
            return filtered
        else:
            err_writer("", pid, response.status_code)

    except Exception as e:
        err_writer(e, pid, response.status_code, file_type)
        # print(f"Request failed with status code: {response.status_code}")

def run_parallel(url_list_batch, file_type='', max_workers=25): #Increase max_workers for faster
    batch_num, batch = url_list_batch
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(extract_api_response, item, batch_num, file_type) for item in batch]
        for future in as_completed(futures):
            try:
                result = future.result()  # just to catch exceptions
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Task failed: {e}")
    return  results

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

#Validation
def check_duplicate_field(data, field_name):
    seen = set()
    for item in data:
        val = item.get(field_name)
        if val in seen:
            return True, val  # Duplicate found
        seen.add(val)
    return False, None
