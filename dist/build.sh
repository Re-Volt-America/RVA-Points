#!/bin/bash

rm -r dist
rm -r build

pyinstaller rva_points.spec -w --onefile

mkdir dist/rva_points
mkdir dist/rva_points/sessions
mkdir dist/rva_points/results

cp -r ../icons dist/rva_points
cp -r ../tracks dist/rva_points
cp -r ../cars dist/rva_points

mv dist/rva_points.exe dist/rva_points
