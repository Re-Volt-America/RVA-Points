import wx

from rva_points_app.logging import print_log


class CarNotFound(Exception):
    def __init__(self, car_name):
        print_log(f"Car '{car_name}' was not found in the car files.")
        print_log(f"The parsing process has been aborted. Please resolve the issues and try again.")

        wx.MessageBox(f"Car '{car_name}' was not found in the car files.\n"
                      f"See the Console for more details.", "Error",
                      wx.OK | wx.ICON_ERROR)


class TrackShortNameNotFound(Exception):
    def __init__(self, track_name):
        print_log(f"No short name found for track '{track_name}'.")

        wx.MessageBox(f"Track '{track_name}' does not have a short name!", "Info",
                      wx.OK | wx.ICON_INFORMATION)


class InvalidRacerTeam(Exception):
    def __init__(self, racer_name):
        print_log(f"Racer {racer_name} does not have a team.")
        print_log(f"Unable to parse session. Either remove the player or add a team tag.")

        wx.MessageBox(f"Racer '{racer_name}' does not have a team!\n"
                      f"See the Console for more details.", "Error",
                      wx.OK | wx.ICON_ERROR)


class NoSessionLog(Exception):
    def __init__(self):
        wx.MessageBox("You must import a session log before exporting!", "Info", wx.OK | wx.ICON_INFORMATION)
