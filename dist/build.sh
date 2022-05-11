#!/bin/bash

[ -e dist ] && rm -r dist
[ -e build ] && rm -r build

pyinstaller rva_points.spec

mkdir dist/rva_points

cp -r ../icons dist/rva_points

mv dist/rva_points.exe dist/rva_points
