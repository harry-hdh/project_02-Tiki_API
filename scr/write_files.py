import json

def response_writer(api_response, pid, batch_num, type=''):
    filename = f"files/{type}api_response_{batch_num}.json"
    with open(filename, 'a', encoding='utf-8') as output_data:
        json.dump(api_response, output_data, ensure_ascii=False)
        output_data.write("\n")
        print("--------------------------------------------\n", "API RESPONSE SAVED:", filename, f"pID: {pid}", "\n--------------------------------------------")

def err_writer(error_msg, pid, status, type=''):
    filename = f"files/{type}error_log.txt"
    with open(filename, 'a', encoding='utf-8') as output_err:
        output_err.write(f"{error_msg} - status {status} - pID: {pid}\n")

#Save last id to file as checkpoint
def save_checkpoint(last_id):
    with open("files/checkpoint.json", "w") as f:
        json.dump({"last_id": last_id}, f)