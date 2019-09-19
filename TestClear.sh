#!/bin/bash
#
# Delete the build folder & external build

rm -rf build
cd external
rm -rf cgns cgnslib_*
