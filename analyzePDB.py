import os
import time
import json
import requests
import concurrent.futures


def get_all_pdb_files():
    files = []
    for dirname, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if ".pdb" not in filename:
                continue
            files.append((filename, dirname))
    print(files)
    return files


def download_file(arg_tuple):
    try:
        filename, dirname = arg_tuple
        print("started working on file", filename)
        file = os.path.join(dirname, filename)

        qmean_url = "https://swissmodel.expasy.org/qmean/submit/"

        response = requests.post(url=qmean_url,
                                 data={"project_name:": "muhi_phd", "email": "spam1010@hotmail.com"},
                                 files={"structure": open(file, 'rb')})

        post_json = response.json()
        results_response = requests.get(post_json["results_json"])
        results_response_json = results_response.json()

        while results_response_json["status"] != "COMPLETED":
            response = requests.get(post_json["results_json"])
            results_response_json = response.json()
            print(filename, "status", results_response_json["status"])
            time.sleep(1)

        json_file_path = os.path.join(dirname, filename.split(".")[0] + ".json")
        print("saving json file", json_file_path)
        with open(json_file_path, 'w') as f:
            models = results_response_json["models"]
            f.write(json.dumps(models))
    except Exception as ex:
        print(ex)


def main():
    files = get_all_pdb_files()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(download_file, files)


main()

