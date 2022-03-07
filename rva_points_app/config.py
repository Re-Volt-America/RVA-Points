import json

from rva_points_app.logging import *


def prepare_config():
    configfile = os.path.join(CONFIG_DIR, "config.json")

    if os.path.isfile(configfile):
        try:
            with open(configfile, "r") as f:
                CONFIG.update(json.load(f))
        except Exception as e:
            print_log(f"Could not load config file.\n  {e}")


def save_config():
    configfile = os.path.join(CONFIG_DIR, "config.json")

    try:
        with open(configfile, "w") as f:
            json.dump(CONFIG, f, indent=4)
    except Exception as e:
        print_log(f"Could not save config file.\n  {e}")
