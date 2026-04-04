from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import re
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from writer import *

session = requests.Session()
retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

def extract_api_response(url, batch_num, file_type=''):
    # response = requests.get(url, headers='')
    global response
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

            response_writer(filtered, pid, batch_num, file_type)
        else:
            err_writer("", pid, response.status_code)

    except Exception as e:
        err_writer(e, pid, response.status_code, file_type)
        # print(f"Request failed with status code: {response.status_code}")

def run_parallel(url_list_batch, file_type='', max_workers=20): #Increase max_workers for faster
    batch_num, batch = url_list_batch
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(extract_api_response, item, batch_num, file_type) for item in batch]
        for future in as_completed(futures):
            try:
                future.result()  # just to catch exceptions
            except Exception as e:
                print(f"Task failed: {e}")