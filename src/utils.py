import asyncio
import aiohttp
import re
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from src.write_files import err_writer

MAX_CONCURRENT_REQUESTS = 25
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
#retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
RETRIABLE_ERRORS = (aiohttp.ClientError, asyncio.TimeoutError)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(RETRIABLE_ERRORS),
    reraise=True # Passes the last error up if all attempts fail
)
async def fetch_with_retry(session, url, headers):
    try:
        async with session.get(url, headers=headers, timeout=20) as response:
            if response.status == 200:
                return await response.json()
            elif response.status in [429, 500, 502, 503, 504]:
                # Force a retry for server-side errors or rate limits
                response.raise_for_status()
    except Exception as e:
        status = getattr(e, 'status', 'N/A')
        err_writer(e, "", status, "")
    return None

async def extract_api_response_async(session, url, batch_num, file_type):
    header = {'User-Agent': 'Mozilla/5.0'}
    pid = url.split("/")[-1]
    async with semaphore:
        try:
            data = await fetch_with_retry(session, url, header)
            if data:
                      # or .text()
                images_list = data.get("images", [])

                filtered = {
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "price": data.get("price"),
                    "url_key": data.get("url_key"),
                    "description": re.sub(r"<.*?>|\n|\r", "", data.get("description") or "").strip(),
                    "image_urls": [img.get("base_url") for img in images_list if
                                    img.get("base_url")] if images_list else []
                }
                return filtered

        except Exception as e:
            status = getattr(e, 'status', 'N/A')
            err_writer(e, pid, "Failed after retries", file_type)
    return None


# 2. The main runner
async def run_parallel_async(url_list_batch, file_type=''):
    batch_num, batch = url_list_batch

    # ClientSession handles connection pooling (reusing connections)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in batch:
            # We create a list of 'coroutine' objects
            task = extract_api_response_async(session, url, batch_num, file_type)
            tasks.append(task)

        # gather() runs them all concurrently and waits for the results
        results = await asyncio.gather(*tasks)

        # Filter out None values (failed requests)
        return [r for r in results if r is not None]

def chunked(lst, size):
    for i in range(0,len(lst), size):
        yield lst[i:i + size]

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