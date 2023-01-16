import json
import requests

from rva_points_app.logging import *

""" Makes sure all folders exist """
def prepare_folders():
    for folder in ["sessions", "results", "data", "logs"]:
        create_folder(os.path.join(CONFIG_DIR, folder))

    create_folder(os.path.join(CONFIG_DIR, "data/version"))

""" Retrieves all the RVA Data files and creates them if they don't exist """
def fetch_data():
    for car_class in RVGL_CAR_CLASSES_NAMES:
        file = f"data/{car_class}.yaml"
        if not os.path.isfile(file):
            r = requests.get(f"{RVA_DATA_URL}/yaml/{car_class}.yaml")
            create_file(f"data/{car_class}.yaml", r.text)

    tracks_file = "data/track_names.yaml"
    if not os.path.isfile(tracks_file):
        r = requests.get(f"{RVA_DATA_URL}/yaml/track_names.yaml")
        create_file(tracks_file, r.text)

    data_version_file = "data/version/rva_data.json"
    if not os.path.isfile(data_version_file):
        r = requests.get(f"{RVA_DATA_URL}/rva_data.json")
        create_file(data_version_file, r.text)


""" Retrieves the data version string from its version folder. If not found, a new data version file is downloaded. """
def get_data_version():
    data_version_file_path = os.path.join(os.getcwd(), "data/version/rva_data.json")
    if not os.path.isfile(data_version_file_path):
        r = requests.get(f"{RVA_DATA_URL}/rva_data.json")
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
        file.writelines(contents)
        print_log(f"Created file '{file.name}'")

    except Exception as e:
        print_log(f"Could not create file '{file}'.\n {e}")
