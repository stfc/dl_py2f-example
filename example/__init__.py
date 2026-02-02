import numpy
import ctypes
import os.path
from . import callback, example_dirs
# system installed DL_PY2F
try:
    import dl_py2f
# DL_PY2F compiled from source code
except:
    from . import dl_py2f
from .example import Example

def doSomething(obj):
    '''We run the Fortran code here and get the number of validation errors as returned value'''

    print(f'\n >>> doSomething (Py): NumPy version = {numpy.__version__}')

    soname = os.path.join(example_dirs.libdir, 'libexample.so')
    libexample = ctypes.CDLL(soname)

    objRef = dl_py2f.py2f(obj, byref=True, debug=0)

    print(f'\n >>> doSomething (Py): calling to the Fortran function interface_example()...')
    nerrors = libexample.interface_example(objRef)

    return nerrors


# not used if the program is started from a user input script
if __name__ == '__main__':

    doSomething()


# for convenience these names can be imported by the user with `from example import *`
__all__ = 'callback', 'doSomething', 'dl_py2f', 'Example'

