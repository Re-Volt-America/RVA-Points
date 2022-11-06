#!/usr/bin/env python3
# RVA Points (Generic)
# Generate json for app info and updates.

import os
import json
import hashlib
import requests

RVA_POINTS_URL = "https://distribute.rva.lat/rva_points/"

def get_checksum(filename):
    try:
        sha = hashlib.sha256()
        with open(filename, 'rb') as f:
            while chunk := f.read(256*1024):
                sha.update(chunk)
        return sha.hexdigest()
    except Exception as e:
        return ""

content = {}
with open(os.path.join("..", "rva_points_app", "version.py")) as f:
    exec(f.read(), content)

version = content["__version__"]

appinfo = {}
appinfo["version"] = version

for platform in ["win64", "linux", "macos"]:
    fname = f"rva_points_{platform}.zip"
    url = f"{RVA_POINTS_URL}{platform}/{fname}"

    response = requests.get(url, stream=True)
    with open(fname, "wb") as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

    appinfo[platform] = {}
    appinfo[platform]["url"] = url
    appinfo[platform]["checksum"] = get_checksum(fname)

with open("rva_points.json", "w") as f:
    json.dump(appinfo, f, indent=4)
