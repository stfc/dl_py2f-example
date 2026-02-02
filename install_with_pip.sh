#!/bin/bash

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

# create a Python virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install dl_py2f

# assuming the current working directory containing the compile.sh script is YOUR_CWD
cwd=$PWD

# build the example project
cd example
rm -rf build
mkdir build
cd build
cmake ..; make

# uncomment to clean
#make clean

# to run the example project and test DL_PY2
# go back to YOUR_CWD
cd $cwd
export PYTHONPATH=$cwd
python3 user_script.py
python3 -c "import dl_py2f; print(f' DL_PY2F location:\n {dl_py2f.__file__}')"

# exit the virtual environment
deactivate

