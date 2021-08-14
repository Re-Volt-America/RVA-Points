import wx

APP_VERSION = "0.0.1-alpha"  # TODO: Fetch version from GitHub

APP_NAME = "rvapp"
APP_TITLE = "RVA Points"
APP_TITLE_WITH_VER = "RVA Points %s" % APP_VERSION

APP_MIN_SIZE = wx.Size(720, 480)
APP_LAUNCH_SIZE = wx.Size(900, 600)

RVA_DEFAULT_CLASS = "rookie"
RVA_CLASSES = ["rookie", "amateur", "advanced", "semi-pro", "pro", "super-pro", "random", "clockwork"]
CAR_CLASSES = ["rookie", "amateur", "advanced", "semi-pro", "pro", "super-pro", "clockwork"]
GITHUB_REPO = "https://github.com/Re-Volt-America/RVA-Points"
GITHUB_ISSUES = "https://github.com/Re-Volt-America/RVA-Points/issues"

CONFIG = {
    "decimal_number_separator": ","
}
