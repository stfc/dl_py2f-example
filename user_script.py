# this script demonstrates how the user launches your application project

from example import *
import numpy, time, sys

t0 = time.time()

# create an instance of <class 'Example'> and initialise its attributes
my_example = Example()
my_example.size = 10
my_example.coords = numpy.arange(30, dtype=float).reshape(10,3)
my_example.tags   = numpy.arange(10)
my_example.c[::2] = 11
#my_example.f[-1,3:-1] = 1000
my_example.zmatrix['j']  = range(my_example.size)
my_example.zmatrix['bond']  = 1.5
my_example.zmatrix['k']  = range(my_example.size)
my_example.zmatrix['angle'] = 90.0
my_example.zmatrix['l']  = range(my_example.size)
my_example.zmatrix['dihedral'] = 180.0

# run the project's function
nerrors = doSomething(my_example)

# verify the array values which were changed in example.f90
assert(my_example.c.tolist() == [2711,0,11,0,11])

# validate tags array which was set to added by 100 in Fortran
tags_ref = list(range(100, 110))
tags_calc = my_example.tags.tolist()
assert tags_calc == tags_ref, f'tags are {tags_calc} but should be {tags_ref}'

# validate Fortran-to-Python interoperability which currently only supports gfortran (nerrors=0)
if not nerrors:
    assert(numpy.all(my_example.angle == 120.0)), f'angle is {my_example.angle} but should be 120.0'
    assert(my_example.coords[0,0] == -1000.0)   , f'coords[0,0] is {my_example.coords[0,0]} but should be -1000.0'
    numpy.testing.assert_allclose(my_example.energy, 6637.433625, atol=1E-6)
# other compilers Intel/flang/NVIDIA are skipped (nerrors>0)
else:
    numpy.testing.assert_allclose(my_example.energy, 6637.433625, atol=1E-6)
    print(f'\n >>> User script (Py): Fortran-to-Python interoperability skipped for unsupported compiler ({nerrors} validation differences as expected)')

print(f'\n Example exiting normally. Total time used: {time.time()-t0} s')

# nvfortran workaround: os._exit() bypasses Python's cleanup which can trigger double-free errors
import os
os._exit(0)
