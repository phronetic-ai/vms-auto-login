import json
import yaml
import subprocess
import time
import os
from pathlib import Path
from datetime import datetime
import requests

COMMON_FILE = "a.txt"
API_URL = "https://devapi.phronetic.ai/admin/web_room/check_feed"
CONFIG_FILE = "config.yaml"

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)

config = load_config()

def is_cctv_active():
    headers = {"Content-Type": "application/json"}
    data = { "webroom_id": config["webroom_id"] }
    response = requests.post(API_URL, headers=headers, json=data)
    if not response.status_code == 200:
        print(f"{datetime.now()} => API failed: {response.status_code}")
        return True
    response = response.json()
    print(f"{datetime.now()} => API response: {response}")
    return response['cctv_status'] == 'true'
    # res = os.path.exists("b.txt")
    # if res:
    #     os.remove("b.txt")
    # return res
    # return True

def create_child_process():
    Path(COMMON_FILE).touch()
    vms_data = json.dumps(config["vms_data"])
    child_process = subprocess.Popen(["python", "child.py", vms_data])
    return child_process

def main():
    sleep_time = config["sleep_time"]
    child_process = create_child_process()
    try:
        while True:
            time.sleep(sleep_time)
            if not is_cctv_active():
                if os.path.exists(COMMON_FILE):
                    os.remove(COMMON_FILE)
                time.sleep(10)
                child_process = create_child_process()
            else:
                print("Condition not met. Continuing to sleep.")
    except KeyboardInterrupt:
        print("Shutting down parent script.")
        child_process.terminate()
        if os.path.exists(COMMON_FILE):
            os.remove(COMMON_FILE)
        try:
            child_process.wait(timeout=10)
            print("Terminated gracefully")
        except subprocess.TimeoutExpired:
            os.kill(child_process.pid, 9)
            print("Child killed")

if __name__ == "__main__":
    main()