import os
import sys
import platform

from appdirs import *
from rva_points_app.version import __version__

APP_NAME = "rvapp"
APP_TITLE = "RVA Points"
APP_TITLE_WITH_VER = "RVA Points %s" % __version__
RVA_POINTS_URL = "https://distribute.rva.lat/rva_points"
RVA_DATA_URL = "https://distribute.rva.lat/rva_data"

# Car classes (rva-specific & rv)
RVA_CLASSES = ["rookie", "amateur", "advanced", "semi-pro", "pro", "super-pro", "random", "clockwork"]
CAR_CLASSES = ["rookie", "amateur", "advanced", "semi-pro", "pro", "super-pro", "clockwork"]

# Internal car class values
CLOCKWORK = -1
ROOKIE = 1
AMATEUR = 2
ADVANCED = 3
SEMI_PRO = 4
PRO = 5
SUPER_PRO = 6
RANDOM = None

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
