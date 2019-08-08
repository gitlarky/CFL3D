#!/bin/bash
#
# How to Install Under Linux
#
# 1: Install Compilation Tools
sudo apt-get install libopenmpi-dev gfortran build-essential cmake git
# 2: Compile it under $HOME Directory
cd $HOME
mkdir cfl3d
cd cfl3d
git clone https://github.com/gitlarky/CFL3D
cd CFL3D/external
./build_cgns
cd ..
mkdir build
cd build
cmake ../
make -j 8
# 3: Move compiled file into /opt and set environment
cd $HOME/cfl3d
sudo cp -rf CFL3D /opt/
cd ..
rm -rf cfl3d
cd /opt/CFL3D
echo "# Add CFL3D executables to PATH">>$HOME/.bashrc
echo 'export PATH=/opt/CFL3D/build/bin:$PATH'>>$HOME/.bashrc
