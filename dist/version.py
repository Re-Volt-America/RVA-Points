#!/usr/bin/env python3
# RVA Points (Windows)
# Generate version file for use with PyInstaller.

import os
from packaging import version

content = {}
with open(os.path.join("..", "rva_points_app", "version.py")) as f:
    exec(f.read(), content)

v = version.parse(content["__version__"])

version_text = f"""
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers={v.release},
    prodvers={v.release},
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904e4', [
        StringStruct(u'FileDescription', u'Re-Volt America Points Calculator'),
        StringStruct(u'FileVersion', u'{v.public}'),
        StringStruct(u'InternalName', u'RVA Points'),
        StringStruct(u'LegalCopyright', u'Copyright (C) BGM 2021-2023'),
        StringStruct(u'OriginalFilename', u'RVA Points'),
        StringStruct(u'ProductName', u'RVA Points'),
        StringStruct(u'ProductVersion', u'{str(v.release)[1:-1]}')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1252])])
  ]
)
"""

with open("version.txt", "w") as f:
    f.write(version_text)
