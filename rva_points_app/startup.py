import json

from rva_points_app.logging import *

import requests

""" Makes sure all folders exist """
def prepare_folders():
    for folder in ["sessions", "results", "data", "logs"]:
        create_folder(os.path.join(CONFIG_DIR, folder))

    create_folder(os.path.join(CONFIG_DIR, "data/version"))


def prepare_data():
    fetch_data(update=False)


" Fetches all data files. In case of an update, it replaces everything "
def fetch_data(update=False):
    for car_class in CAR_CLASSES:
        file = f"data/{car_class}.yaml"
        if update:
            r = requests.get(f"{APP_DATA_URL}/{car_class}.yaml")
            create_file(f"data/{car_class}.yaml", r.text)
        else:
            if not os.path.isfile(file):
                r = requests.get(f"{APP_DATA_URL}/{car_class}.yaml")
                create_file(f"data/{car_class}.yaml", r.text)

    tracks_file = "data/track_names.yaml"
    if update:
        r = requests.get(f"{APP_DATA_URL}/track_names.yaml")
        create_file(tracks_file, r.text)
    else:
        if not os.path.isfile(tracks_file):
            r = requests.get(f"{APP_DATA_URL}/track_names.yaml")
            create_file(tracks_file, r.text)

    data_version_file = "data/version/rva_points_data.json"
    if update:
        r = requests.get(f"{APP_DATA_URL}/rva_points_data.json")
        create_file(data_version_file, r.text)
    else:
        if not os.path.isfile(tracks_file):
            r = requests.get(f"{APP_DATA_URL}/rva_points_data.json")
            create_file(data_version_file, r.text)

""" Retrieves the data version number from its version folder. If not found, a new data version file is downloaded. """
def get_data_version():
    data_version_file_path = os.path.join(os.getcwd(), "data/version/rva_points_data.json")
    if not os.path.isfile(data_version_file_path):
        r = requests.get(f"{APP_DATA_URL}/rva_points_data.json")
        create_file(data_version_file_path, r.text)

    with open(data_version_file_path, "r") as f:
        data_version_json = json.load(f)

    return data_version_json["version"]


""" Creates a folder if it does not exist """
def create_folder(folder):
    if not os.path.isdir(folder):
        try:
            os.makedirs(folder)
            print_log(f"Created folder '{folder}'")
        except Exception as e:
            print_log(f"Could not create folder '{folder.name}'.\n  {e}")


""" Creates a file """
def create_file(file, contents):
    try:
        file = open(file, 'w')
        file.writelines(contents.split("\n"))
        print_log(f"Created file '{file.name}'")

    except Exception as e:
        print_log(f"Could not create file '{file}'.\n {e}")