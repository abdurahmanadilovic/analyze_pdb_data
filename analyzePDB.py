import os
import time
import json
import requests
import concurrent.futures
from threading import Lock

print_lock = Lock()
qmean_url = "https://swissmodel.expasy.org/qmean/submit/"


def print_concurrent(*msg):
    with print_lock:
        print(msg)


def get_all_pdb_files():
    files = []
    for dirname, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if ".pdb" not in filename:
                continue
            files.append((filename, dirname))
    print_concurrent(files)
    return files


def submit_file_and_get_results_json(file):
    post_request = requests.post(url=qmean_url,
                                 data={"project_name:": "muhi_phd", "email": "spam1010@hotmail.com"},
                                 files={"structure": open(file, 'rb')})
    post_request_json = post_request.json()

    return post_request_json["results_json"], requests.get(post_request_json["results_json"]).json()


def download_file(arg_tuple):
    try:
        filename, dirname = arg_tuple
        print_concurrent("started working on file", filename)

        file = os.path.join(dirname, filename)
        results_url, results_response_json = submit_file_and_get_results_json(file)

        sleep_in_seconds = 10
        while results_response_json["status"] != "COMPLETED":
            results_response_json = requests.get(results_url).json()
            print_concurrent(filename, "status", results_response_json["status"])

            if results_response_json["status"] == "FAILED":
                sleep_in_seconds *= 2
                print_concurrent(filename, "status FAILED", "sleeping for", sleep_in_seconds, "seconds")
                time.sleep(sleep_in_seconds)
                results_url, results_response_json = submit_file_and_get_results_json(file)
                continue

            time.sleep(sleep_in_seconds)

        json_file_path = os.path.join(dirname, filename.split(".")[0] + ".json")
        print_concurrent("saving json file", json_file_path)
        with open(json_file_path, 'w') as f:
            models = results_response_json["models"]
            f.write(json.dumps(models))
    except Exception as ex:
        print_concurrent(ex)


def main():
    files = get_all_pdb_files()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(download_file, files)


main()
