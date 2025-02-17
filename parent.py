import subprocess
import time
import os
from pathlib import Path
from datetime import datetime
import requests

COMMON_FILE = "a.txt"

def is_cctv_active():
    url = "https://devapi.phronetic.ai/admin/web_room/check_feed"
    headers = {"Content-Type": "application/json"}
    data = { "webroom_id": "67a078c396cb9f44a4156666" }
    response = requests.post(url, headers=headers, json=data)
    if not response.status_code == 200:
        print(f"{datetime.now()} => API failed: {response.status_code}")
        return True
    response = response.json()
    print(f"{datetime.now()} => CCTV Status: {response['cctv_status']}")
    return response['cctv_status'] == 'true'
    # res = os.path.exists("b.txt")
    # if res:
    #     os.remove("b.txt")
    # return res
    # return True

def create_child_process():
    Path(COMMON_FILE).touch()
    child_process = subprocess.Popen(["python", "child.py"])
    return child_process

def main():
    sleep_time = 600
    child_process = create_child_process()
    try:
        while True:
            time.sleep(sleep_time)  # Sleep for 10 minutes initially and then 5 mins
            if not is_cctv_active():
                if os.path.exists(COMMON_FILE):
                    os.remove(COMMON_FILE)
                time.sleep(10)
                child_process = create_child_process()
            else:
                print("Condition not met. Continuing to sleep.")
            sleep_time = 600
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