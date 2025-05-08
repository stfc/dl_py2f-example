# this script demonstrates how the user launches your application project

from example import *
import numpy

# create an instance of <class 'Example'> and initialise it
my_example = Example()
my_example.size = 10
my_example.coords = numpy.arange(30, dtype=float).reshape(10,3)
my_example.tags   = numpy.arange(10)

# run the project's function
doSomething(my_example)

