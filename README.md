<p align="center">
  <img height="200" width="200" src="https://user-images.githubusercontent.com/26081543/129637656-c5014e3e-cdf6-4437-9e0d-157bc63c14e7.png" />
</p>


<h1 align="center">RVA-Points</h1>
<h4 align="center">A program to parse <a href="https://rvgl.re-volt.io/" target="_blank">RVGL</a> session logs and export them as Re-Volt America results</h4>


## Installation
  1. Download the latest release available [here](https://distribute.revolt-america.com/rva_points/rva_points-latest.zip). It should come as a compressed file.
  2. De-compress the files into a folder anywhere in your system.
  3. Execute `rva_points.exe`.
      * We currently only support Windows


## Preview Images
<p align="left">
  <h3>Calculate Tab</h3>
  <img src="https://user-images.githubusercontent.com/26081543/156964493-974875a8-057f-4a7e-9611-d7b08f7520da.PNG" alt=""/>
  <h3>Preview Tab</h3>
  <img src="https://user-images.githubusercontent.com/26081543/156964394-2d2588f8-4e86-4b23-98ab-94c3532a049d.PNG" alt=""/>
</p>

### Running
Software you will need in order to run the program in development mode.

- [Python 3.8 or above](https://www.python.org/downloads/)
- Python modules:
  - wxPython
  - PyYAML
  - requests
  - PyInstaller (we use it for dist)
- We suggest the usage of venv & pip for development & dependency management. (In case of Apple Silicon use conda)
