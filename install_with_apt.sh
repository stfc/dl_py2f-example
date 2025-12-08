#!/bin/bash

# sudo access is needed to install DL_PY2F for the system
sudo add-apt-repository ppa:dl-py2f/ppa
sudo apt update
sudo apt upgrade
# please note it's a hyphen "-" here as an underscore "_" doesn't exist in PPA repos
sudo apt install dl-py2f

# assuming the current working directory containing the compile.sh script is YOUR_CWD
cwd=$PWD

# build the example project
cd example
rm -rf dl_py2f
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
echo $cwd
python3 user_script.py
echo  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo  Please note apt-installed DL_PY2F works only with projects compiled with gfortran!
echo  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
python3 -c "import dl_py2f; print(f' DL_PY2F location:\n {dl_py2f.__file__}')"
