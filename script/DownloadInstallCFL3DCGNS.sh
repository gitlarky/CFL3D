#!/bin/bash
#
# How to install under Linux
# when
#     1: not having the whole CFL3D package downloaded except this bash file
#     2: planning to develop CFL3D project
#
# 1: Install Compilation Tools
sudo apt-get install libopenmpi-dev gfortran build-essential cmake git
# 2: Compile it under $HOME Directory
cd $HOME
mkdir gitlarky
cd gitlarky
git clone https://github.com/gitlarky/CFL3D
cd CFL3D/external
./build_cgns
cd ..
mkdir build
cd build
cmake ../
make -j 8
# 3: Move compiled file into /opt and set environment
cd $HOME/gitlarky
sudo cp -rf CFL3D /opt/
cd /opt/CFL3D
echo "# Add CFL3D executables to PATH">>$HOME/.bashrc
echo 'export PATH=/opt/CFL3D/build/bin:$PATH'>>$HOME/.bashrc
