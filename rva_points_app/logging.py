"""
Name: widgets.py
Author: https://gitlab.com/re-volt/rvgl-launcher/-/blob/master/rv_launcher/logging.py
"""

import os
import sys
import threading

from datetime import datetime
from traceback import print_exc
from rva_points_app import common
from rva_points_app.common import *
from rva_points_app.version import __version__


""" File logging class """
class LogFile:
    lock = threading.Lock()
    buffer = []

    def __init__(self):
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"log_{time}.txt"

        self.path = os.path.join(CONFIG_DIR, "logs", self.filename)
        self.write_out(f"Initializing log file: {self.path}\n\n")

        try:
            with open(self.path, "w", encoding="utf-8") as f:
                f.write(f"RVGL Launcher Log File\n")
        except Exception as e:
            self.write_out(f"Could not initialize log file.\n  {e}\n")

        self.write(f"App Path: {get_app_path()}\n")
        self.write(f"Build: v{__version__}\n")
        self.write(f"Platform: {PLATFORM}\n\n")

    """ Writes a log entry to file and stdout """
    def write(self, line):
        self.write_out(line)
        self.write_file(line)

    """ Writes a log entry to file """
    def write_file(self, line):
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception as e:
            self.write_out(f"Could not write to log file.\n  {e}\n")

    """ Writes a log entry to stdout and UI buffer """
    def write_out(self, line):
        LogFile.buffer.append(line)
        # Do not print to stdout on Windows because of the fixed size buffer
        # issue that affects windowed applications (our PyInstaller bundle).
        # https://stackoverflow.com/a/13430732
        if sys.platform != "win32":
            print(line, end="")

    """ Flushes the UI buffer to the passed control """
    @staticmethod
    def print_ctrl(ctrl):
        if not LogFile.buffer:
            return

        with LogFile.lock:
            ctrl.write("".join(LogFile.buffer))
            LogFile.buffer.clear()

    """ Prints a log message to multiple handlers """
    @staticmethod
    def print_log(*line):
        with LogFile.lock:
            print(*line, file=common.log_file)

    """ Prints exception trace to multiple handlers """
    @staticmethod
    def print_trace():
        with LogFile.lock:
            print_exc(file=common.log_file)

    """ Loads log file content from disk """
    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            self.write_out(f"Could not load log file.\n  {e}\n")
            return ""

    """ Saves log file content to disk """
    def save(self, content):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            self.write_out(f"Could not save log file.\n  {e}\n")


""" Wrappers to print log messages and exceptions """
def print_log(*line):
    LogFile.print_log(*line)


def print_trace():
    LogFile.print_trace()
