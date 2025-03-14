import numpy
import ctypes
import os.path
import dl_py2f
import example_dirs

def doSomething(obj):

    print(f'\n >>> doSomething (Py): NumPy version = {numpy.__version__}')

    soname = os.path.join(example_dirs.libdir, 'libexample.so')
    libexample = ctypes.CDLL(soname)

    objRef = dl_py2f.py2f(obj, byref=True, debug=0)

    print(f'\n >>> doSomething (Py): calling to the Fortran function interface_example()...')
    ierror = libexample.interface_example(objRef)

# not used if the program is started from a user input script
if __name__ == '__main__':

    doSomething()

__all__ = 'doSomething', 'dl_py2f'

