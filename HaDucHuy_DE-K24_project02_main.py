import time
from scr.read_files import read_product_id_csv, read_error_ids, load_checkpoint
from pathlib import Path
from scr.main_funcs import *
from scr.write_files import save_checkpoint

# Read products
product_ids = read_product_id_csv('products-0-200000.csv')

# def main(pid_list):
#     last_id = load_checkpoint("./files/checkpoint.json")
#     start = False if last_id else True
#
#     for i, batch in enumerate(chunked(get_prod_url(pid_list), 1000), 1):
#         if not start:
#             if last_id in batch:
#                 start = True
#                 batch = batch[batch.index(last_id) + 1:]
#             else:
#                 continue
#         try:
#             # chunk the list to smaller batches low
#
#             run_parallel((i, batch))
#             save_checkpoint(batch[-1])
#
#         except Exception as e:
#             print(f"Error on batch {i}: {e}")
#             time.sleep(2)  # basic retry delay
#             raise  # IMPORTANT → let Supervisor restart
#
# if __name__ == '__main__':
#     main(product_ids)

for i, batch in enumerate(chunked(get_prod_url(product_ids), 10), 1):
    run_parallel((i, batch))
#Check if error log exists
file_path = Path("./files/error_log.txt")
if file_path.is_file():
    # Retry error products
    err_product_ids = read_error_ids(file_path)
    for i, batch in enumerate(chunked(get_prod_url(err_product_ids), 500), 1):
        run_parallel((i, batch),'RETRY')