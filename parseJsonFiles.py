import os
import json
import csv


def build_csv_dict(data, final_dict):
    for key in data:
        if isinstance(data[key], dict):
            if key == 'local_scores':
                inner_dict = data[key]
                inner_dict['local_scores'] = inner_dict[list(inner_dict.keys())[0]]
                del inner_dict[list(inner_dict.keys())[0]]
                build_csv_dict(inner_dict, final_dict)
            else:
                build_csv_dict(data[key], final_dict)
        else:
            if isinstance(data[key], str):
                final_dict[key] = data[key].rstrip()
            else:
                final_dict[key] = data[key]

    return final_dict


def main():
    json_files = []

    for dirname, dirnames, filenames in os.walk('./files'):

        for filename in filenames:
            if ".json" not in filename:
                continue

            file = os.path.join(dirname, filename)

            with open(file, 'r') as f:
                data = json.load(f)

            csv_file_path = os.path.join(dirname, filename.split(".")[0] + ".csv")
            json_files.append((csv_file_path, build_csv_dict(data, {})))

    with open(os.path.join('.', 'files', 'results.csv'), 'w') as file:
        results_file = csv.writer(file)
        results_file.writerow(json_files[0][1].keys())
        for json_file in json_files:
            results_file.writerow(json_file[1].values())


main()
