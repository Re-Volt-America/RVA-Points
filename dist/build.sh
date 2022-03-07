#!/bin/bash

rm -r dist
rm -r build

pyinstaller rva_points.spec -w --onefile

mkdir dist/rva_points

cp -r ../icons dist/rva_points

mv dist/rva_points.exe dist/rva_points
