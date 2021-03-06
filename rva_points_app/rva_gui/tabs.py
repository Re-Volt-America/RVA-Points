from threading import Thread

import wx.grid as grid
import subprocess

from rva_points_app.rva_gui.widgets import *
from rva_points_app.session_log import SessionLog
from rva_points_app.updates import *


class CalculateTab(ScrolledTabPage):
    def __init__(self, parent):
        TabPage.__init__(self, parent)
        self.init_ui()
        self.session = None
        self.session_file_name = None
        self.session_file_path = None
        self.teams = CONFIG["teams"]
        self.allows_mystery = False

    def init_ui(self):
        self.box = wx.BoxSizer(wx.VERTICAL)

        self.init_calculate_ui()

        self.box.Add(self.box_calculate, 1, wx.EXPAND)

        self.SetSizer(self.box)

    def init_calculate_ui(self):
        self.box_calculate = wx.BoxSizer(wx.VERTICAL)

        " Select Category Grid "
        self.box_calculate_header = wx.GridSizer(rows=1, cols=1, vgap=30, hgap=30)
        self.box_class_selection = wx.BoxSizer(wx.VERTICAL)
        self.box_class_selector = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1, "Select Category:")
        self.box_class_selector.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.class_options = [clazz.capitalize() for clazz in RVA_CLASSES]
        self.class_selector = wx.Choice(self, -1, choices=self.class_options)
        self.class_selector.Bind(wx.EVT_CHOICE, self.on_class_selection)
        self.box_class_selector.Add(self.class_selector, 1, wx.EXPAND | wx.ALL, 5)
        self.box_class_selection.Add(self.box_class_selector, 0, wx.EXPAND, 0)

        self.box_calculate_header.Add(self.box_class_selection, 1, wx.EXPAND, 0)
        self.box_calculate.Add(self.box_calculate_header, 0, wx.EXPAND | wx.ALL, 10)

        " Actions Grid "
        self.box_actions_header = wx.GridSizer(rows=1, cols=3, vgap=0, hgap=0)

        " Actions Box "
        self.box_actions = wx.StaticBoxSizer(wx.VERTICAL, self, "Actions")
        self.box_actions.SetMinSize(wx.Size(300, 50))
        static_box = self.box_actions.GetStaticBox()

        self.box_import_string = wx.BoxSizer(wx.HORIZONTAL)
        self.import_string = wx.StaticText(static_box, -1, "Import Session Log")
        self.import_button = wx.Button(static_box, -1, "Import")
        self.import_button.Bind(wx.EVT_BUTTON, self.on_import_button_click)
        self.box_import_string.Add(self.import_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_import_string.Add(self.import_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_actions.Add(self.box_import_string, 1, wx.EXPAND | wx.ALL, 0)

        self.box_export_string = wx.BoxSizer(wx.HORIZONTAL)
        self.export_string = wx.StaticText(static_box, -1, "Export Session Log")
        self.export_button = wx.Button(static_box, -1, "Export")
        self.export_button.Bind(wx.EVT_BUTTON, self.on_export_button_click)
        self.box_export_string.Add(self.export_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_export_string.Add(self.export_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_actions.Add(self.box_export_string, 1, wx.EXPAND | wx.ALL, 0)

        self.box_calculate_string = wx.BoxSizer(wx.HORIZONTAL)
        self.calculate_string = wx.StaticText(static_box, -1, "Process and Calculate")
        self.calculate_button = wx.Button(static_box, -1, "Calculate")
        self.calculate_button.Bind(wx.EVT_BUTTON, self.on_calculate_button_click)
        self.box_calculate_string.Add(self.calculate_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_calculate_string.Add(self.calculate_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_actions.Add(self.box_calculate_string, 1, wx.EXPAND | wx.ALL, 0)

        self.box_preview_string = wx.BoxSizer(wx.HORIZONTAL)
        self.preview_string = wx.StaticText(static_box, -1, "Preview RVA Results")
        self.preview_button = wx.Button(static_box, -1, "Preview")
        self.preview_button.Bind(wx.EVT_BUTTON, self.on_preview_button_click)
        self.box_preview_string.Add(self.preview_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_preview_string.Add(self.preview_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_actions.Add(self.box_preview_string, 1, wx.EXPAND | wx.ALL, 0)

        self.box_teams_string = wx.BoxSizer(wx.HORIZONTAL)
        self.teams_string = wx.StaticText(static_box, -1, "Teams Session")
        self.teams_checkbox = wx.CheckBox(static_box, -1, label="")
        self.teams_checkbox.Bind(wx.EVT_CHECKBOX, self.on_teams_check_mark)
        self.teams_checkbox.SetValue(CONFIG["teams"])
        self.box_teams_string.Add(self.teams_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_teams_string.Add(self.teams_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_actions.Add(self.box_teams_string, 1, wx.EXPAND | wx.ALL, 0)

        self.box_allow_mystery_string = wx.BoxSizer(wx.HORIZONTAL)
        self.allow_mystery_string = wx.StaticText(static_box, -1, "Allow Mystery")
        self.allow_mystery_checkbox = wx.CheckBox(static_box, -1, label="")
        self.allow_mystery_checkbox.Bind(wx.EVT_CHECKBOX, self.on_allow_mystery_check_mark)
        self.allow_mystery_checkbox.Disable()
        self.box_allow_mystery_string.Add(self.allow_mystery_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_allow_mystery_string.Add(self.allow_mystery_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_actions.Add(self.box_allow_mystery_string, 1, wx.EXPAND | wx.ALL, 0)

        "Update Box"
        self.box_update = wx.StaticBoxSizer(wx.VERTICAL, self, "Update")
        self.box_update.SetMinSize(wx.Size(300, 50))
        static_box = self.box_update.GetStaticBox()

        self.box_update_parser_string = wx.BoxSizer(wx.HORIZONTAL)
        self.update_parser_string = wx.StaticText(static_box, -1, "Checking for updates...")
        self.update_parser_button = wx.Button(static_box, -1, "Update")
        self.update_parser_button.Disable()
        self.update_parser_button.Bind(wx.EVT_BUTTON, self.on_update_parser_button_click)
        self.box_update_parser_string.Add(self.update_parser_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_update_parser_string.Add(self.update_parser_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_update.Add(self.box_update_parser_string, 1, wx.EXPAND | wx.ALL, 0)

        self.box_update_data_string = wx.BoxSizer(wx.HORIZONTAL)
        self.update_data_string = wx.StaticText(static_box, -1, "Checking for updates...")
        self.update_data_button = wx.Button(static_box, -1, "Update")
        self.update_data_button.Disable()
        self.update_data_button.Bind(wx.EVT_BUTTON, self.on_update_data_button_click)
        self.box_update_data_string.Add(self.update_data_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_update_data_string.Add(self.update_data_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_update.Add(self.box_update_data_string, 1, wx.EXPAND | wx.ALL, 0)

        " Quick Access Box "
        self.box_quick_access = wx.StaticBoxSizer(wx.VERTICAL, self, "Quick Access")
        self.box_quick_access.SetMinSize(wx.Size(300, 50))
        static_box = self.box_quick_access.GetStaticBox()

        self.box_open_sessions_string = wx.BoxSizer(wx.HORIZONTAL)
        self.open_sessions_string = wx.StaticText(static_box, -1, "Sessions Folder")
        self.open_sessions_button = wx.Button(static_box, -1, "Open")
        self.open_sessions_button.Bind(wx.EVT_BUTTON, self.on_open_sessions_button_click)
        self.box_open_sessions_string.Add(self.open_sessions_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_open_sessions_string.Add(self.open_sessions_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_quick_access.Add(self.box_open_sessions_string, 1, wx.EXPAND | wx.ALL, 0)

        self.box_open_results_string = wx.BoxSizer(wx.HORIZONTAL)
        self.open_results_string = wx.StaticText(static_box, -1, "Results Folder")
        self.open_results_button = wx.Button(static_box, -1, "Open")
        self.open_results_button.Bind(wx.EVT_BUTTON, self.on_open_results_button_click)
        self.box_open_results_string.Add(self.open_results_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_open_results_string.Add(self.open_results_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_quick_access.Add(self.box_open_results_string, 1, wx.EXPAND | wx.ALL, 0)

        self.box_open_parser_string = wx.BoxSizer(wx.HORIZONTAL)
        self.open_parser_string = wx.StaticText(static_box, -1, "Parser Folder")
        self.open_parser_button = wx.Button(static_box, -1, "Open")
        self.open_parser_button.Bind(wx.EVT_BUTTON, self.on_open_parser_button_click)
        self.box_open_parser_string.Add(self.open_parser_string, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_open_parser_string.Add(self.open_parser_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.box_quick_access.Add(self.box_open_parser_string, 1, wx.EXPAND | wx.ALL, 0)

        self.box_actions_header.Add(self.box_actions, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        self.box_actions_header.Add(self.box_quick_access, 1, wx.ALIGN_LEFT | wx.ALL, 1)
        self.box_actions_header.Add(self.box_update, 2, wx.ALIGN_LEFT | wx.ALL, 2)
        self.box_calculate.Add(self.box_actions_header, 0, wx.EXPAND | wx.ALL, 5)

        self.set_class(RVA_CLASSES[CONFIG["default_category"]])
        self.check_for_updates()

    def on_class_selection(self, e):
        if e is None:
            print_log(f"Selected Class: '{RVA_CLASSES[CONFIG['default_category']].capitalize()}'")
        else:
            print_log(f"Selected Class: '{e.GetString()}'")

    def on_import_button_click(self, e):
        self.parent.parent.on_import_session_log(e)

    def on_export_button_click(self, e):
        self.parent.parent.on_export_session_log(e)

    def on_calculate_button_click(self, e):
        if self.session is None:
            return

        print_log(f"Calculating Results...")

        new_log = SessionLog(self.session_file_path, teams=self.is_parsing_teams())
        self.session = new_log.get_session()
        self.session.rva_system.set_category_class_number(self.get_selected_class_number())
        self.session.rva_system.set_allows_mystery(self.allows_mystery)

        self.update_preview()

    def on_preview_button_click(self, e):
        self.on_calculate_button_click(self)

        index = self.parent.FindPage(self.frame.preview_tab)
        self.parent.SetSelection(index)

    def on_teams_check_mark(self, e):
        self.teams = not self.teams
        CONFIG["teams"] = self.teams

    def on_allow_mystery_check_mark(self, e):
        self.allows_mystery = not self.allows_mystery

    def on_update_parser_button_click(self, e):
        parser_update_thread = Thread(target=update_parser, args=[self.update_parser_button, self.update_parser_string])
        parser_update_thread.start()

    def on_update_data_button_click(self, e):
        data_update_thread = Thread(target=update_data, args=[self.update_data_button, self.update_data_string])
        data_update_thread.start()

    def on_open_parser_button_click(self, e):
        msg = ""
        directory = os.path.join(os.getcwd())
        file = ""
        wildcard = ""
        dialog = wx.FileDialog(self, msg, directory, file, wildcard)
        response = dialog.ShowModal()

        if response == wx.ID_OK:
            if sys.platform == "win32":
                os.startfile(dialog.GetPath())
            elif sys.platform in ["linux", "darwin"]:
                subprocess.call(["open", dialog.GetPath()])

    def on_open_sessions_button_click(self, e):
        msg = ""
        directory = os.path.join(os.getcwd(), "sessions")
        file = ""
        wildcard = ""
        dialog = wx.FileDialog(self, msg, directory, file, wildcard)
        response = dialog.ShowModal()

        if response != wx.ID_OK:
            return

        if sys.platform == "win32":
            os.startfile(dialog.GetPath())
        elif sys.platform in ["linux", "darwin"]:
            error = subprocess.call(["open", dialog.GetPath()])
            if error:
                # This causes a Warning to be thrown on mac for some reason? Minor, but should be resolved
                wx.MessageBox(f"No application associated to {dialog.Filename}'s file type", "Info",
                              wx.OK | wx.ICON_INFORMATION)

    def on_open_results_button_click(self, e):
        msg = ""
        directory = os.path.join(os.getcwd(), "results")
        file = ""
        wildcard = ""
        dialog = wx.FileDialog(self, msg, directory, file, wildcard)
        response = dialog.ShowModal()

        if response != wx.ID_OK:
            return

        if sys.platform == "win32":
            os.startfile(dialog.GetPath())
        elif sys.platform in ["linux", "darwin"]:
            error = subprocess.call(["open", dialog.GetPath()])
            if error:
                wx.MessageBox(f"No application associated to {dialog.Filename}'s file type", "Info",
                              wx.OK | wx.ICON_INFORMATION)

    def set_class(self, car_class):
        if car_class is not None:
            car_class.capitalize()

        car_class = (RVA_CLASSES[CONFIG["default_category"]].capitalize(), car_class)[car_class in self.class_options]
        if car_class in self.class_options:
            self.class_selector.SetSelection(self.class_options.index(car_class))
            self.on_class_selection(None)

    def check_for_updates(self):
        parser_update_check_thread = Thread(target=parser_update_available, args=[self.update_parser_button, self.update_parser_string])
        parser_update_check_thread.start()

        data_update_check_thread = Thread(target=data_update_available, args=[self.update_data_button, self.update_data_string])
        data_update_check_thread.start()

    def get_selected_class_number(self):
        return self.class_selector.GetSelection()

    def is_parsing_teams(self):
        return self.teams

    def update_preview(self):
        if self.session is None:
            return

        preview_tab = self.parent.parent.preview_tab
        preview_tab.update_preview(self.session)


class PreviewTab(ScrolledTabPage):
    def __init__(self, parent):
        TabPage.__init__(self, parent)
        self.rva_results = None

        self.GRID_BACKGROUND_RGB = wx.Colour(45, 63, 67)
        self.GRID_BORDER_RGB = wx.Colour(100, 100, 100)
        self.GRID_CELL_HIGHLIGHT_RGB = wx.Colour(255, 253, 1)

        self.GRID_COL_HEADER_BACKGROUND_RGB = wx.Colour(29, 40, 43)
        self.GRID_COL_HEADER_RGB = wx.Colour(255, 217, 102)

        self.GRID_COL_POS_RGB = wx.Colour(255, 217, 102)
        self.GRID_COL_CONTENT_RGB = wx.Colour(144, 96, 0)

        self.GRID_RACER_NAME_RGB = wx.Colour(189, 215, 238)
        self.GRID_POS_RGB = wx.Colour(91, 173, 169)
        self.GRID_FIRST_PLACE_RGB = wx.Colour(255, 215, 0)
        self.GRID_SECOND_PLACE_RGB = wx.Colour(204, 204, 204)
        self.GRID_THIRD_PLACE_RGB = wx.Colour(205, 127, 50)
        self.GRID_INVALID_PLACE_RGB = wx.Colour(255, 50, 40)

        self.init_ui()

    def init_ui(self):
        self.box = wx.BoxSizer(wx.VERTICAL)

        self.init_preview_ui()

        self.box.Add(self.box_preview, 1, wx.EXPAND)

        self.SetSizer(self.box)

    def init_preview_ui(self):
        self.box_preview = wx.BoxSizer(wx.VERTICAL)
        self.box_preview_header = wx.GridSizer(rows=1, cols=1, vgap=30, hgap=30)

        self.box_session_grid = wx.BoxSizer(wx.VERTICAL)
        self.session_grid = grid.Grid(self)
        self.session_grid.CreateGrid(6, 6)
        self.__set_default_preview()

        self.box_preview_header.Add(self.session_grid, 1, wx.EXPAND, 0)
        self.box_preview.Add(self.box_preview_header, 1, wx.EXPAND | wx.ALL, 10)

    def update_preview(self, session):
        if session.teams:
            self.rva_results = session.get_rva_teams_results_arr()
        else:
            self.rva_results = session.get_rva_singles_results_arr()

        rows = len(self.rva_results) - 1
        cols = len(self.rva_results[0])

        self.__reset_preview()
        self.__update_grid_size(rows, cols)
        self.__fill_and_style_preview_col_headers()
        self.__fill_preview_content()
        self.__style_preview_content()

    def __fill_and_style_preview_col_headers(self):
        head_col = 0
        for row in self.rva_results[:1]:
            for item in row:
                if head_col == 0:
                    self.session_grid.SetColSize(head_col, 30)
                    self.session_grid.SetColLabelValue(head_col, str(item))
                if head_col == 1:
                    self.session_grid.SetColSize(head_col, 150)
                    self.session_grid.SetColLabelValue(head_col, str(item))
                else:
                    short_name = str(item)
                    if short_name is not None:
                        self.session_grid.SetColSize(head_col, 30)
                        self.session_grid.SetColLabelValue(head_col, short_name)
                    elif str(item) == "Team":
                        self.session_grid.SetColLabelValue(head_col, str(item))
                    else:
                        self.session_grid.SetColLabelValue(head_col, str(item))
                    if str(item) in ["PP", "PA", "CC", "MP", "PO"]:
                        self.session_grid.SetColSize(head_col, 80)
                    if str(item) == "Team":
                        self.session_grid.SetColSize(head_col, 40)

                head_col = head_col + 1

    def __fill_preview_content(self):
        grid_row = 0
        for row in self.rva_results[1:]:
            grid_col = 0
            for item in row:
                if grid_col == 0:
                    self.session_grid.SetColSize(grid_col, 25)
                    self.session_grid.SetRowSize(grid_row, 25)
                self.session_grid.SetCellValue(grid_row, grid_col, str(item))
                grid_col = grid_col + 1
            grid_row = grid_row + 1

    def __style_preview_content(self):
        for row in range(0, self.session_grid.GetNumberRows()):
            reached_end_of_cars_row = False
            current_car_col_size = 1
            current_car_col = None
            current_car = None
            for col in range(0, self.session_grid.GetNumberCols()):
                if col == 0:
                    self.session_grid.SetCellTextColour(row, col, self.GRID_COL_CONTENT_RGB)
                    self.session_grid.SetCellBackgroundColour(row, col, self.GRID_COL_POS_RGB)
                    self.session_grid.SetCellFont(row, col, wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
                    self.session_grid.SetCellAlignment(row, col, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
                elif col == 1:
                    self.session_grid.SetCellTextColour(row, col, self.GRID_POS_RGB)
                    self.session_grid.SetCellBackgroundColour(row, col, self.GRID_BACKGROUND_RGB)
                    self.session_grid.SetCellFont(row, col, wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
                    self.session_grid.SetCellAlignment(row, col, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
                else:
                    self.session_grid.SetCellTextColour(row, col, self.GRID_POS_RGB)
                    self.session_grid.SetCellBackgroundColour(row, col, self.GRID_BACKGROUND_RGB)
                    self.session_grid.SetCellFont(row, col, wx.Font(10, wx.SWISS, wx.ITALIC, wx.BOLD))

                    if row % 2 == 0:  # Even rows are used for places
                        self.session_grid.SetCellAlignment(row, col, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
                        if self.session_grid.GetCellValue(row, col).startswith("'"):
                            self.session_grid.SetCellTextColour(row, col, self.GRID_INVALID_PLACE_RGB)
                            continue

                        if self.session_grid.GetColLabelValue(col) in ["PP", "PA", "CC", "MP", "PO"]:
                            continue

                        try:
                            place = int(self.session_grid.GetCellValue(row, col))
                            if place == 1:
                                self.session_grid.SetCellTextColour(row, col, self.GRID_FIRST_PLACE_RGB)
                            elif place == 2:
                                self.session_grid.SetCellTextColour(row, col, self.GRID_SECOND_PLACE_RGB)
                            elif place == 3:
                                self.session_grid.SetCellTextColour(row, col, self.GRID_THIRD_PLACE_RGB)
                        except ValueError:
                            pass
                    else:  # Odd rows are used for car names
                        if self.session_grid.GetCellValue(row, col) == " ":
                            reached_end_of_cars_row = True

                        if not reached_end_of_cars_row:
                            if current_car is None and self.session_grid.GetCellValue(row, col) == str():
                                continue
                            elif current_car is None and self.session_grid.GetCellValue(row, col) != str():
                                current_car = self.session_grid.GetCellValue(row, col)
                                current_car_col = col
                                if self.session_grid.GetCellValue(row, col + 1) == str():
                                    current_car_col_size = current_car_col_size + 1
                                else:
                                    self.session_grid.SetCellSize(row, current_car_col, 1, current_car_col_size)
                                    current_car = self.session_grid.GetCellValue(row, col + 1)
                                    current_car_col = col + 1
                                    current_car_col_size = 1
                            else:
                                if self.session_grid.GetCellValue(row, col + 1) == str():
                                    current_car_col_size = current_car_col_size + 1
                                else:
                                    self.session_grid.SetCellSize(row, current_car_col, 1, current_car_col_size)
                                    current_car = self.session_grid.GetCellValue(row, col + 1)
                                    current_car_col = col + 1
                                    current_car_col_size = 1

    def __reset_preview(self):
        self.session_grid.ClearGrid()

        rows = self.session_grid.GetNumberRows()
        cols = self.session_grid.GetNumberCols()

        for i in range(0, rows):
            for j in range(0, cols):
                self.session_grid.SetCellSize(i, j, 1, 1)

        self.__set_default_preview()
        self.session_grid.SetColLabelSize(30)

    def __set_default_preview(self):
        rows = 6
        cols = 6

        self.__update_grid_size(rows, cols)
        self.session_grid.SetGridLineColour(self.GRID_BORDER_RGB)
        self.session_grid.SetCellHighlightColour(self.GRID_CELL_HIGHLIGHT_RGB)

        for i in range(0, rows):
            for j in range(0, cols):
                self.session_grid.SetCellBackgroundColour(i, j, self.GRID_BACKGROUND_RGB)

        for i in range(0, rows):
            self.session_grid.SetRowSize(i, 25)

        for i in range(0, cols):
            self.session_grid.SetColSize(i, 75)

        self.session_grid.HideRowLabels()
        self.session_grid.HideColLabels()
        self.session_grid.SetLabelBackgroundColour(self.GRID_COL_HEADER_BACKGROUND_RGB)
        self.session_grid.SetLabelTextColour(self.GRID_COL_HEADER_RGB)

    def __update_grid_size(self, rows, cols):
        current_row_count = self.session_grid.GetNumberRows()

        if rows < current_row_count:
            self.session_grid.DeleteRows(0, current_row_count - rows, True)
        elif rows > current_row_count:
            self.session_grid.AppendRows(rows - current_row_count)

        current_col_count = self.session_grid.GetNumberCols()

        if cols < current_col_count:
            self.session_grid.DeleteCols(0, current_col_count - cols, True)
        elif cols > current_col_count:
            self.session_grid.AppendCols(cols - current_col_count)


class ConsoleTab(TabPage):
    def __init__(self, parent):
        TabPage.__init__(self, parent)
        self.init_ui()

    def init_ui(self):
        self.box = wx.BoxSizer(wx.VERTICAL)

        self.text_console = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        self.box.Add(self.text_console, 1, wx.EXPAND | wx.ALL, 5)

        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000)

        self.SetSizer(self.box)

    def on_timer(self, e):
        LogFile.print_ctrl(self.text_console)
