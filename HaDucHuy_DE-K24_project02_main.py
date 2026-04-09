import time
from scr.read_files import read_product_id_csv, read_error_ids, load_checkpoint
from pathlib import Path
from scr.main_funcs import *
from scr.write_files import save_checkpoint, response_writer

# Read products
product_ids = read_product_id_csv('products-0-200000.csv')

def main(pid_list):
    file_path = Path("./files/checkpoint.json")

    if file_path.is_file():
        last_id = load_checkpoint(file_path)
    else:
        last_id = None

    start = False if last_id else True

    for i, batch in enumerate(chunked(get_prod_url(pid_list), 1000), 1):

        if not start:
            match_index = next((idx for idx, url in enumerate(batch) if last_id in url), None)

            if match_index is not None:
                start = True
                batch = batch[match_index + 1:]
            else:
                continue

        if not batch:
            continue

        retries = 3
        for attempt in range(retries):
            try:
                batch_results = run_parallel((i, batch))
                response_writer(batch_results, i)
                save_checkpoint(batch[-1])
                break
            except Exception as e:
                print(f"Error on batch {i}, attempt {attempt + 1}: {e}")
                time.sleep(2)
                if attempt == retries - 1:
                    raise

def retry_pipeline():
    # Check if error log exists to rerun errors
    file_path = Path("./files/error_log.txt")
    if not file_path.is_file():
        print("No error log found")
        return
    err_product_ids = read_error_ids(file_path)
    if not err_product_ids:
        # Retry error products
        print("No failed IDs to retry")
        return
    #Clear old error log BEFORE retry
    file_path.unlink(missing_ok=True)
    for i, batch in enumerate(chunked(get_prod_url(err_product_ids), 500), 1):
        results = run_parallel((i, batch), 'RETRY')

        if results:
            response_writer(results, f"retry_{i}")

if __name__ == '__main__':
    main(product_ids)
    retry_pipeline()
# for i, batch in enumerate(chunked(get_prod_url(product_ids), 1000), 1):
#     batch_results = run_parallel((i, batch))
#     response_writer(batch_results, i)
