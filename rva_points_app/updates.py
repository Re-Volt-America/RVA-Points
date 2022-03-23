import requests
import wx

from rva_points_app.startup import *
from rva_points_app.version import __version__


def parser_update_available(button, text):
    r = requests.get(f"{RVA_POINTS_URL}/rva_points.json")
    if r.status_code == 200:
        version = r.json()["version"]
        if version != __version__:
            wx.CallAfter(button.Enable)
            wx.CallAfter(text.SetLabelText, f"Parser v{version} is available!")
            print_log(f"New Parser version detected: {version}")
        else:
            wx.CallAfter(text.SetLabelText, f"Parser is up to date.")
    else:
        print_log(f"Unable to retrieve data update. Error {r.status_code}.")
        wx.CallAfter(text.SetLabelText, f"Unable to retrieve update info.")


def data_update_available(button, text):
    r = requests.get(f"{RVA_DATA_URL}/rva_data.json")
    if r.status_code == 200:
        version = r.json()["version"]
        if version != get_data_version():
            wx.CallAfter(button.Enable)
            wx.CallAfter(text.SetLabelText, f"Data v{version} is available!")
            print_log(f"New RVA Data version detected: {version}")
        else:
            wx.CallAfter(text.SetLabelText, f"RVA Data is up to date.")
    else:
        print_log(f"Unable to retrieve RVA Data update. Error {r.status_code}.")
        wx.CallAfter(text.SetLabelText, "Unable to retrieve update info.")


def update_parser(button, text):
    wx.CallAfter(button.Disable)
    wx.CallAfter(text.SetLabelText, "Updating...")

    if sys.platform == "win32":
        executable = "rva_points.exe"
        url = f"{RVA_POINTS_URL}/{executable}"
    else:
        executable = "rva_points"
        url = f"{RVA_POINTS_URL}/{executable}"

    # Cannot replace a running application on Windows
    # but renaming should work
    if sys.platform == "win32":
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
    if r.status_code == 200:
        open(executable, 'wb').write(r.content)

        wx.CallAfter(text.SetLabelText, "Pending restart.")
        wx.MessageBox("Parser has been updated.\nRestart to begin using the new version.", "Info", wx.OK | wx.ICON_INFORMATION)

        wx.Exit()
        os.startfile(executable)
    else:
        print_log(f"Unable to retrieve parser update. Error {r.status_code}.")
        wx.CallAfter(button.Enable)
        wx.CallAfter(text.SetLabelText, "Unable to retrieve update info.")


def update_data(button, text):
    wx.CallAfter(button.Disable)
    wx.CallAfter(text.SetLabelText, "Updating...")

    fetch_data(update=True)

    wx.CallAfter(button.Enable)
    wx.CallAfter(text.SetLabelText, "Data is up to date.")
