# DL_PY2F Example

[![GNU](https://github.com/stfc/dl_py2f-example/actions/workflows/gnu.yml/badge.svg)](https://github.com/stfc/dl_py2f-example/actions/workflows/gnu.yml)

# About

This package contains a toy application which uses [`DL_PY2F`](https://github.com/stfc/dl_py2f-example) for the interoperability in both Python-to-Fortran and Fortran-to-Python ways.

## License

`DL_PY2F example` is open source and released under [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html). It is available for download from the [repository](https://github.com/stfc/dl_py2f-example).

## Citing `DL_PY2F`

Applications using `DL_PY2F` should cite:

You Lu and Thomas W. Keal, *Journal of Open Source Software*, in preparation

## Project status

The Python-to-Fortran interoperability demonstrated in `DL_PY2F example` has been comprehensively tested using both GNU and Intel compilers.

:warning: **Warning:** However, the method for Fortran-to-Python interoperability demonstrated in `DL_PY2F example` is still undergoing testing and validation, and is currently limited to use with the GNU compiler gfortran, as the proprietary .mod file format used by the Intel compiler is not yet supported.

# Getting started

## Required libraries and tools


| Tools & Libraries             | Min. version | Note |
|:------------------------------|:-------------|:-----|
| gcc/gfortran                  | 7.3          |      |
| OR icc/ifort                  | 17           | :warning: |
| cmake                         | 3.16         |      |
| python3-dev                   | 3.8          |      |
| python3-numpy                 | 1.21.5       |      |

:bulb: The above package names are based on Ubuntu Linux. They may vary on other
       operating systems.

:warning: The Fortran-to-Python method does **NOT** yet work with the Intel compilers as Intel's proprietary
          .mod file format is unpublished and unsupported.

## Compiling

For compiling and running this example application using `DL_PY2F`, please follow the steps (bash environment assumed here)

1. Cloning the example package to, e.g., `my_copy` (you probably have done this already):

`$ git clone https://github.com/stfc/dl_py2f-example.git my_copy`

2. Navigating to the example package's source package (which contains this _README.md_ file):

`$ cd my_copy`

3. There is a subdirectory for an example application project:

`$ cd example`

4. Cloning `DL_PY2F` from the repository:

`$ git clone git clone https://github.com/stfc/dl_py2f.git dl_py2f`

5. Making a directory for building

`$ mkdir build`

`$ cd build`

6. Configuring and compiling using cmake

`$ cmake ..; make`

## Running

There is an exemplar user input script for launching the example project. To run it, please

1. Navigating to the example package's source package (which contains the current _README.md_ file):

`$ cd my_copy`

2. Define the environment variable `PYTHONPATH` for the example application project:

`$ export PYTHONPATH=my_copy`

3. Run as a user of your example application:

`$ python3 user_script.py`

:bulb: For using `DL_PY2F` in your own real project, there are more ways to organise the source package's structure.

## Cleaning

`$ cd example/build`

`$ make clean`

:bulb: There is also a bash script _compile.sh_ containing all the above steps which is ready for executing.

# Miscellaneous

## Support

Please raise an Issue on the [project's page](https://github.com/stfc/dl_py2f-example) if you have a question about the code.

## Contributing

Contributions are welcome in the form of Issue/PR on [github.com](https://github.com/stfc/dl_py2f-example).

## Acknowledgements

The `DL_PY2F` library was created during the redevelopment of [ChemShell](https://chemshell.org) as a Python-based package, which was funded by EPSRC under the grant [EP/K038419/1](https://gtr.ukri.org/projects?ref=EP/K038419/1). Ongoing support for the development of `DL_PY2F` as part of ChemShell is provided under EPSRC grants [EP/R001847/1](https://gtr.ukri.org/projects?ref=EP%2FR001847%2F1) and [EP/W014378/1](https://gtr.ukri.org/projects?ref=EP%2FW014378%2F1), and the [Computational Science Centre for Research Communities (CoSeC)](https://www.cosec.ac.uk), via the support provided to the [Materials Chemistry Consortium](https://mcc.hec.ac.uk). We acknowledge helpful discussions and suggestions for improvement from Paul Sherwood, Joseph Thacker, and Thomas Durrant.
