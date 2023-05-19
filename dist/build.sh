#!/bin/bash

for i in "$@"; do
  case $i in
    --linux) linux=linux;;
    --macos) macos=macos;;
    --win32) win32=win32;;
    --win64) win32=win64;;
    --build) build=true;;
    --clean) clean=true;;
  esac
done

if [ "$clean" = true ]; then
  rm -f *.zip *.gz *.txt *.json
  rm -rf win32/build
  rm -rf win64/build
  rm -rf macos/build
  rm -f win32/rva_points.exe
  rm -f win64/rva_points.exe
  rm -rf macos/rva_points.app
  rm -f macos/rva_points
  rm -f win32/helper.exe
  rm -f win64/helper.exe
fi

if [ "$build" = true ]; then
  python=python
  if [ "$PYTHONPATH" ]; then
    python="${PYTHONPATH}/python"
  fi

  python version.py # Always use native python

  if [ "$linux" ]; then
    "python" -m PyInstaller rva_points_${linux}.spec --workpath ${linux}/build --distpath ${linux} --windowed
  fi

  if [ "$macos" ]; then
    "python" -m PyInstaller rva_points_${macos}.spec --workpath ${macos}/build --distpath ${macos} --windowed
  fi

  if [ "$win32" ]; then
    "${python}.exe" -m PyInstaller rva_points_${win32}.spec --workpath ${win32}/build --distpath ${win32}
  fi
fi
