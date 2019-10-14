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
    for dirname, dirnames, filenames in os.walk('./files'):

        for filename in filenames:
            if ".json" not in filename:
                continue

            file = os.path.join(dirname, filename)

            with open(file, 'r') as f:
                data = json.load(f)

            csv_file_path = os.path.join(dirname, filename.split(".")[0] + ".csv")
            with open(csv_file_path, 'w') as file:
                csv_dict = build_csv_dict(data, {})
                json_file = csv.writer(file)
                json_file.writerow(csv_dict.keys())
                json_file.writerow(csv_dict.values())


main()

