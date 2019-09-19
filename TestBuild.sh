#!/bin/bash
#
# How to install under Linux 
# when 
#     1: having the whole CFL3D package downloaded from github.com/gitlarky/CFL3D
#     2: not planning to develope the CFL3D project
#
# 1: Install Compilation Tools
sudo apt-get install libopenmpi-dev gfortran build-essential cmake git
# 2: Compile it under $HOME Directory
cd external
./build_cgns
cd ..
mkdir build
cd build
cmake ../
make -j 8

