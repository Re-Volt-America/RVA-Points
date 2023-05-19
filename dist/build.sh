#!/bin/bash

for i in "$@"; do
  case $i in
    --linux) linux=linux;;
    --macos) macos=macos;;
    --win32) win32=win32;;
    --win64) win32=win64;;
    --build) build=true;;
    --package) package=true;;
    --release) release=true;;
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

if [ "$package" = true ]; then
  files="icons rva_points_app rva_points.py"

  if [ "$linux" ]; then
    rm -f rva_points_${linux}.zip
    (cd .. && dist/${linux}/7zz a dist/rva_points_${linux}.zip -r ${files} -x\!"*__pycache__*")
  fi

  if [ "$macos" ]; then
    rm -f rva_points_${macos}.zip
    (cd .. && dist/${macos}/7zz a dist/rva_points_${macos}.zip -r ${files} -x\!"*__pycache__*")
  fi

  if [ "$win32" ]; then
    rm -f rva_points_${win32}.zip
    (cd .. && dist/${win32}/7z.exe a dist/rva_points_${win32}.zip -r ${files} -x\!"*__pycache__*")
  fi
fi

# Run after having used --build!
#
if [ "$release" = true ]; then
  if [ "$linux" ]; then
    rm -f rva_points_${linux}_release.zip
    (cd .. && dist/${linux}/7zz a dist/rva_points_${linux}_release.zip icons ./dist/${linux}/rva_points  -x\!"*__pycache__*")
  fi

  if [ "$macos" ]; then
    rm -f rva_points_${macos}_release.zip
    (cd .. && dist/${macos}/7zz a dist/rva_points_${macos}_release.zip ./dist/${macos}/RVA\ Points.app -x\!"*__pycache__*")
  fi

  if [ "$win32" ]; then
    rm -f rva_points_${win32}_release.zip
    (cd .. && dist/${win32}/7z.exe a dist/rva_points_${win32}_release.zip icons ./dist/${win32}/rva_points.exe -x\!"*__pycache__*")
  fi
fi
