# this script demonstrates how the user launches your application project

from example import *
import numpy

# create an instance of <class 'Example'> and initialise its attributes
my_example = Example()
my_example.size = 10
my_example.coords = numpy.arange(30, dtype=float).reshape(10,3)
my_example.tags   = numpy.arange(10)
my_example.c[::2] = 11
my_example.f[-1,3:5] = 1000
my_example.zmatrix['j']  = range(my_example.size)
my_example.zmatrix['bond']  = 1.5
my_example.zmatrix['k']  = range(my_example.size)
my_example.zmatrix['angle'] = 90.0
my_example.zmatrix['l']  = range(my_example.size)
my_example.zmatrix['dihedral'] = 180.0

# run the project's function
doSomething(my_example)

# verify the array values which were changed in example.f90
assert(my_example.c.tolist() == [2711,0,11,0,11])
# verify the angles' values which were changed in example.f90
assert(numpy.all(my_example.angle == 120.0))
# verify the coordinate which was changed in example.f90
assert(my_example.coords[0,0] == -1000.0)
# verify the final energy
numpy.testing.assert_allclose(my_example.energy, 6637.433625, atol=1E-6)

print('\n Example exiting normally.')
