#!/bin/bash
# assuming the current working directory containing the compile.sh script is YOUR_CWD
cwd=$PWD

# download DL_PY2F and build the example project
cd example
rm -rf dl_py2f
rm -rf build
mkdir build
git clone https://github.com/stfc/dl_py2f.git dl_py2f
cd build
cmake -DFROM_SOURCE:BOOL=TRUE ..; make

# to clean
#make clean

# to run/test the example project
# go back to YOUR_CWD
cd $cwd
export PYTHONPATH=$cwd
echo $cwd
python3 user_script.py
