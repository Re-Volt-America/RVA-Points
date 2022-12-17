import wx

from packaging import version
from rva_points_app.startup import *
from rva_points_app.version import __version__


def parser_update_available(button, text):
    r = requests.get(f"{RVA_POINTS_URL}/rva_points.json")

    if r.status_code != 200:
        print_log(f"Unable to retrieve data update. Error {r.status_code}.")
        wx.CallAfter(text.SetLabelText, f"Unable to retrieve update info.")
        return

    v = r.json()["version"]
    if version.parse(v) > version.parse(__version__):
        wx.CallAfter(button.Enable)
        wx.CallAfter(text.SetLabelText, f"Parser v{v} is available!")
        print_log(f"New Parser version detected: {v}")
    else:
        wx.CallAfter(text.SetLabelText, f"Parser is up to date.")
        wx.CallAfter(button.Disable)
        print_log(f"Parser is up to date.")


def data_update_available(button, text):
    r = requests.get(f"{RVA_DATA_URL}/rva_data.json")

    if r.status_code != 200:
        print_log(f"Unable to retrieve RVA Data update. Error {r.status_code}.")
        wx.CallAfter(text.SetLabelText, "Unable to retrieve update info.")
        return

    v = r.json()["version"]
    if version.parse(v) > version.parse(get_data_version()):
        wx.CallAfter(button.Enable)
        wx.CallAfter(text.SetLabelText, f"Data v{v} is available!")
        print_log(f"New RVA Data version detected: {v}")
    else:
        wx.CallAfter(text.SetLabelText, f"RVA Data is up to date.")
        wx.CallAfter(button.Disable)
        print_log(f"RVA Data is up to date.")


def update_parser(button, text):
    if os.path.isdir(".git"):
        print_log("Skipping update check in development repo.")
        wx.CallAfter(button.Disable)
        wx.CallAfter(text.SetLabelText, "Skipped in dev repo.")
        return

    wx.CallAfter(button.Disable)
    wx.CallAfter(text.SetLabelText, "Updating...")

    if sys.platform == "win32":
        executable = "rva_points.exe"
        url = f"{RVA_POINTS_URL}/win64/{executable}"
    elif sys.platform == "linux":
        executable = "rva_points"
        url = f"{RVA_POINTS_URL}/linux/{executable}"
    # elif sys.platform == "darwin": FIXME: This needs to be implemented, but im too lazy lol

    # Cannot replace a running application on Windows
    # but renaming should work
    if sys.platform in ['win32', 'linux']:
        bakfile = f"{executable}.bak"
        try:
            if os.path.isfile(bakfile):
                os.remove(bakfile)
            if os.path.isfile(executable):
                os.rename(executable, bakfile)
        except Exception as e:
            print_log(f"Could not create backup file.\n  {e}")
            return

    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        print_log(f"Unable to retrieve parser update. Error {r.status_code}.")
        wx.CallAfter(button.Enable)
        wx.CallAfter(text.SetLabelText, "Unable to retrieve update info.")
        return

    open(executable, 'wb').write(r.content)

    wx.CallAfter(text.SetLabelText, "Pending restart.")
    wx.MessageBox("Parser has been updated.\nRestart to begin using the new version.", "Info",
                  wx.OK | wx.ICON_INFORMATION)

    if sys.platform == 'win32':
        wx.Exit()
        os.startfile(executable)


def update_data(button, text):
    wx.CallAfter(button.Disable)
    wx.CallAfter(text.SetLabelText, "Updating...")

    for car_class in CAR_CLASSES:
        r = requests.get(f"{RVA_DATA_URL}/yaml/{car_class}.yaml")
        create_file(f"data/{car_class}.yaml", r.text)

    tracks_file = "data/track_names.yaml"
    r = requests.get(f"{RVA_DATA_URL}/yaml/track_names.yaml")
    create_file(tracks_file, r.text)

    data_version_file = "data/version/rva_data.json"
    r = requests.get(f"{RVA_DATA_URL}/rva_data.json")
    create_file(data_version_file, r.text)

    wx.CallAfter(text.SetLabelText, "Data is up to date.")
