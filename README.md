<p align="center">
  <img alt="" height="200" width="200" src="https://user-images.githubusercontent.com/26081543/129637656-c5014e3e-cdf6-4437-9e0d-157bc63c14e7.png" />
</p>

<h1 align="center">RVA-Points</h1>
<h4 align="center">A program to parse <a href="https://rvgl.re-volt.io/" target="_blank">RVGL</a> session logs and export them as Re-Volt America results</h4>

<p align="center">
  <a href="https://github.com/Re-Volt-America/RVA-Points/actions/workflows/deploy.yml" class="rich-diff-level-one"><img src="https://github.com/Re-Volt-America/RVA-Points/actions/workflows/deploy.yml/badge.svg?branch=production" alt="deploy" style="max-width:100%;"></a>
  <a href="https://gitlicense.com/license/Re-Volt-America/RVA-Points"><img src="https://gitlicense.com/badge/Re-Volt-America/RVA-Points" alt=""/></a>
</p>

## Installation
  1. Download the latest release for your platform available [here](https://distribute.revolt-america.com/rva_points/).
  2. Depending on your platform:
     * Windows: Execute `rva_points.exe`.
     * Linux: Run `rva_points` from commandline (you may need to grant permissions).
     * MacOS: Decompress & use the application by double clicking rva_points.

## Preview Images
<div align="left">
  <h3>Calculate Tab</h3>
  <img src="https://user-images.githubusercontent.com/26081543/156964493-974875a8-057f-4a7e-9611-d7b08f7520da.PNG" alt=""/>
  <h3>Preview Tab</h3>
  <img src="https://user-images.githubusercontent.com/26081543/156964394-2d2588f8-4e86-4b23-98ab-94c3532a049d.PNG" alt=""/>
</div>

### Running
Software you will need in order to run the program in development mode.

- [Python 3.8 or above](https://www.python.org/downloads/)
- Python modules:
  - wxPython
  - PyYAML
  - requests
  - packaging
  - PyInstaller (we use it for dist)
- We suggest the usage of venv & pip for development & dependency management. (In case of Apple Silicon use conda)
