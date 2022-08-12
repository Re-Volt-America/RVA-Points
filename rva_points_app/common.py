import os
import sys
import platform

from appdirs import *
from rva_points_app.version import __version__

APP_NAME = "rvapp"
APP_TITLE = "RVA Points"
APP_TITLE_WITH_VER = "RVA Points %s" % __version__
RVA_POINTS_URL = "https://distribute.revolt-america.com/rva_points"
RVA_DATA_URL = "https://distribute.revolt-america.com/rva_data"

RVA_CLASSES = ["rookie", "amateur", "advanced", "semi-pro", "pro", "super-pro", "random", "clockwork"]
CAR_CLASSES = ["rookie", "amateur", "advanced", "semi-pro", "pro", "super-pro", "clockwork"]

CONFIG_DIR = os.curdir

if sys.platform == "linux":
    PLATFORM = "linux"
elif sys.platform == "win32":
    if platform.architecture()[0] == "64bit":
        PLATFORM = "win64"
    else:
        PLATFORM = "win32"
elif sys.platform == "darwin":
    PLATFORM = "macos"

log_file = None

CONFIG = {
    "decimal_number_separator": ",",
    "default_category": 0,
    "app_min_window_size": (1000, 480),
    "app_launch_window_size": (1000, 600),
    "show-console": False,
    "teams": False,
    "import_dir": "",
    "export_dir": "",
    "sessions_dir": "",
    "results_dir": ""
}

""" Returns the application base folder """
def get_app_path():
    return sys.path[0]
