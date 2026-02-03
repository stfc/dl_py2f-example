#!/bin/bash
# assuming the current working directory containing the compile.sh script is YOUR_CWD
cwd=$PWD

# download DL_PY2F and build the example project
cd example

rm -rf dl_py2f
git clone https://github.com/stfc/dl_py2f.git dl_py2f

rm -rf build
mkdir build
cd build

# GNU compilers
export FC=gfortran
export CXX=g++
# uncomment to use Intel compilers
#export FC=ifx
#export CXX=icpx
# uncomment to use Flang/Clang++ compilers
#export FC=flang-22
#export CXX=clang++-22
# uncomment to use NVIDIA HPC compilers
#export FC=nvfortran
#export CXX=nvc++

cmake -DFROM_SOURCE:BOOL=TRUE ..; make

# to clean
#make clean

# to run/test the example project
# go back to YOUR_CWD
cd $cwd
export PYTHONPATH=$cwd
echo $cwd
python3 user_script.py
