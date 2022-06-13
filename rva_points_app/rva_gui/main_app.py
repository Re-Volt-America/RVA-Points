import csv
import webbrowser

from rva_points_app.config import prepare_config, save_config
from rva_points_app.rva_gui.tabs import *
from rva_points_app.common import *
from rva_points_app.startup import prepare_folders


class FrameMain(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(FrameMain, self).__init__(*args, **kwargs)
        self.resized = False

        self.init_ui()

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_IDLE, self.on_idle)

    def on_size(self, e):
        self.Layout()

        # When resizing the app's Window, the scrollbars at the Preview tab
        # disappear, even if the grid is too big to be displayed. This
        # makes it so the scrollbars are kept there if they are needed.
        w, h = self.preview_tab.GetMinSize()
        self.preview_tab.SetVirtualSize(w, h)
        self.preview_tab.frame.SetSize(w, h)

        self.resized = True

    def on_idle(self, e):
        if self.resized:
            self.resized = False

    def init_ui(self):
        self.SetTitle(APP_TITLE_WITH_VER)
        self.set_icon()

        self.SetMinSize(wx.Size(CONFIG["app_min_window_size"]))
        self.SetSize(wx.Size(CONFIG["app_launch_window_size"]))
        self.Center()

        self.box = wx.BoxSizer(wx.VERTICAL)

        self.tab_bar = TabBar(self)
        self.calculate_tab = CalculateTab(self.tab_bar)
        self.preview_tab = PreviewTab(self.tab_bar)
        self.console_tab = ConsoleTab(self.tab_bar)

        self.tab_bar.AddPage(self.calculate_tab, "Calculate")
        self.tab_bar.AddPage(self.preview_tab, "Preview")
        self.tab_bar.AddPage(self.console_tab, "Console")
        self.console_tab.Hide()

        self.box.Add(self.tab_bar, 1, wx.EXPAND, 0)
        self.SetSizer(self.box)

        self.init_menubar()

    def init_menubar(self):
        self.menu_bar = wx.MenuBar()

        " File "
        self.menu_files = wx.Menu()

        self.menu_files_import_session_log = self.menu_files.Append(-1, "Import Session Log", "Open session log csv file")
        self.Bind(wx.EVT_MENU, self.on_import_session_log, self.menu_files_import_session_log)

        self.menu_files_export_session_log = self.menu_files.Append(-1, "Export Session Log", "Generate RVA session csv file")
        self.Bind(wx.EVT_MENU, self.on_export_session_log, self.menu_files_export_session_log)

        self.menu_files.AppendSeparator()

        self.menu_files_quit = self.menu_files.Append(wx.ID_EXIT, "Quit", "Quit application")
        self.Bind(wx.EVT_MENU, self.on_quit, self.menu_files_quit)

        self.menu_bar.Append(self.menu_files, "&File")

        " Help "
        self.menu_help = wx.Menu()
        self.menu_help_report_bug = self.menu_help.Append(-1, "Report a Bug", "Opens our GitHub Issues page")
        self.Bind(wx.EVT_MENU, self.on_report_a_bug, self.menu_help_report_bug)

        self.menu_help.AppendSeparator()

        self.menu_help_console = self.menu_help.AppendCheckItem(-1, "Show Console", "Show console messages")
        self.Bind(wx.EVT_MENU, self.on_show_console, self.menu_help_console)
        self.menu_help_console.Check(CONFIG["show-console"])
        self.on_show_console(None)

        self.menu_bar.Append(self.menu_help, "&Help")

        self.SetMenuBar(self.menu_bar)

    def on_import_session_log(self, e):
        msg = "Select Session Log"
        directory = os.path.join(os.getcwd(), "sessions")
        file = ""
        wildcard = "Session Log (*.csv)|*.csv"
        dialog = wx.FileDialog(self, msg, directory, file, wildcard)
        response = dialog.ShowModal()

        if response == wx.ID_OK:
            print_log(f"Importing Session Log '{dialog.GetPath()}'...")

            self.calculate_tab.session = SessionLog(dialog.GetPath(), teams=self.calculate_tab.is_parsing_teams()).get_session()
            self.calculate_tab.session_file_name = dialog.GetFilename()
            self.calculate_tab.session_file_path = dialog.GetPath()
            self.calculate_tab.session.rva_system.set_category_class_number(self.calculate_tab.get_selected_class_number())
            self.calculate_tab.on_preview_button_click(e)
            self.calculate_tab.allows_mystery = False
            self.calculate_tab.allow_mystery_checkbox.Set3StateValue(wx.CHK_UNCHECKED)
            self.calculate_tab.allow_mystery_checkbox.Enable()

        dialog.Destroy()
        self.calculate_tab.update_preview()

    def on_export_session_log(self, e):
        session = self.calculate_tab.session
        if session is None:
            wx.MessageBox("You must import a session log before exporting!", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        msg = "Save file as..."
        directory = os.path.join(os.getcwd(), "results")
        file = "rva-" + self.calculate_tab.session_file_name
        style = wx.FD_SAVE
        wildcard = "Session Log (*.csv)|*.csv"
        dialog = wx.FileDialog(self, msg, directory, file, wildcard, style)
        response = dialog.ShowModal()

        if response == wx.ID_OK:
            print_log(f"Exporting Session Log to '{dialog.GetPath()}'...")

            with open(os.path.join(dialog.GetDirectory(), file), "w+", newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerows(self.calculate_tab.session.get_rva_results())
                csv_file.close()

        dialog.Destroy()

    def on_quit(self, e):
        self.Close()
        e.Skip()

    def on_report_a_bug(self, e):
        webbrowser.open(CONFIG["git_issues_url"])

    def on_show_console(self, e):
        CONFIG["show-console"] = self.menu_help_console.IsChecked()
        if sys.platform != "win32":
            self.console_tab.Show(CONFIG["show-console"])
            return

        # Page hiding is not supported on Windows...
        page = self.tab_bar.FindPage(self.console_tab)
        if CONFIG["show-console"] and page == -1:
            self.tab_bar.AddPage(self.console_tab, "Console")
        elif not CONFIG["show-console"] and page != -1:
            self.tab_bar.RemovePage(page)

    def set_icon(self):
        ext = ("png", "ico")[sys.platform == "win32"]
        icon_file = os.path.join("icons", f"icon.{ext}")
        if os.path.isfile(icon_file):
            self.SetIcon(wx.Icon(icon_file))


def main():
    app = wx.App()

    prepare_config()
    prepare_folders()
    fetch_data()

    common.log_file = LogFile()

    app.SetAppName(APP_NAME)
    app.SetAppDisplayName(APP_TITLE)
    app.SetClassName(APP_TITLE)

    frame = FrameMain(None)
    frame.Show()

    app.SetTopWindow(frame)
    app.MainLoop()

    save_config()


if __name__ == '__main__':
    main()
