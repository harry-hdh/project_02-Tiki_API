import json
import os

def response_writer(batch_results, batch_num, file_type=''):
    filename = f"./files/{file_type}api_response_{batch_num}.json"
    os.makedirs("files", exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as output_data:
        json.dump(batch_results, output_data, ensure_ascii=False, indent=2)

    print("--------------------------------------------\n", "API RESPONSE SAVED: ", filename, "\n--------------------------------------------")

def err_writer(error_msg, pid, status, file_type=''):
    filename = f"./files/{file_type}error_log.txt"
    os.makedirs("files", exist_ok=True)
    with open(filename, 'a', encoding='utf-8') as output_err:
        output_err.write(f"{error_msg} - status {status} - pID: {pid}\n")

#Save last id to file as checkpoint
def save_checkpoint(last_id):
    os.makedirs("files", exist_ok=True)
    pid = last_id.split("/")[-1]
    with open("./files/checkpoint.json", "w") as f:
        json.dump({"last_id": pid}, f)