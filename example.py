import ctypes
import numpy
from numpy import dtype, float64, full, int64, zeros
import dl_py2f
from . import callback

# it has to be a child class of ctypes.Structure
class Example(ctypes.Structure):

    # these entities (of which the order doesn't matter) will be available as member objects
    # to be passed to Fortran and they can be optionally associated with a @property
    # decorator (a setter is mandatory)
    # NB: currently we support only 1- and 2-D arrays
    _kwargs = {
                # an array can be independent from self._master
                'a'       : zeros(shape=(1)  ,      dtype=float64),
                'b'       : zeros(shape=(1)  ,      dtype=float64),
                'callback': callback.callback,
                # NB: as part of self._master, all dtypes must be 64-bit to be aligned in memory!
                'coords'  : zeros(shape=(1,3),      dtype=float64),
                'arr'     : zeros(shape=(1,9),      dtype=int64),
                'c'       : zeros(shape=(5)  ,      dtype=int64),
                'd'       : zeros(shape=(12) ,      dtype=float64),
                'e'       : zeros(shape=(18) ,      dtype=float64),
                # NB: we have to use a one-element array to make its value writeable in Fortran because
                # scalars such as float are immutable in Python!
                'energy'  : zeros(shape=(1)  ,      dtype=float64),
                'factors' : zeros(shape=(1,) ,      dtype=float64),
                # WARNING: only the first characters of each element can be passed to Fortran
                'names'   : full((1)         , 'A', dtype='S8'),
                # other scalar values can be passed to Fortran but note that they are immutable in Python
                # (to make their values altered please use a one-element array such as `energy` above)
                'scale'   : 1.23456,
                # normally the size of self._master is important
                'size'    : 0,
                'tags'    : zeros(shape=(1,)  ,      dtype=int64),
                # we can even embed another struectured array in self._master
                'zmatrix' : zeros(shape=(1,)  ,      dtype=dtype([('j'       ,int64),
                                                                  ('bond'    ,float64),
                                                                  ('k'       ,int64),
                                                                  ('angle'   ,float64),
                                                                  ('l'       ,int64),
                                                                  ('dihedral',float64)])),
              }

    # a master array of the numpy.recarray type will be created as self._master containing
    # the following fields (in the given sequence)
    _fields     = 'names', 'factors', 'coords', 'tags', 'names', 'tags', 'arr', 'zmatrix'

    # initialisation (by @dl_py2f.utils.objutils.init()) of entities defined in this sequence
    # will be prioritised, typically to deal with dependencies
    _priorities = 'coords', 'tags'

    # dicts of entities to be initialised
    _init       = '_kwargs', '_internals'

    # the sequences to be concatenated when we have children classes (not shown in this example)
    _inherit    = '_init', '_priorities'

    # entities to be initialised but not passed to Fortran (typically used internally)
    _internals  = {}

    # for example, _synons = {'coords':'cartesian'} makes only "cartesian" visible in Fortran
    _synons     = {}


    # use this facility decorator to help initialise the values defined in self._kwargs and save a lot of troubles
    @dl_py2f.utils.objutils.init()
    def __init__(self, *args, **kwargs):
        '''Initialise'''


    @property
    def __all__(self):
        ''''''

        return sorted(list(self._kwargs.keys()))


    @property
    def callback(self):
        '''Return the Python callback function'''

        return self._callback


    @callback.setter
    def callback(self, val):
        '''Setter of Python callback function'''

        self._callback = val

        # keep a reference to the current instance so that we will
        # have access to the data when the Python callback function
        # is run by Fortran methods
        self._callback.obj = self


    # defining a @property/setter will be convenient though not necessary
    @property
    def coords(self):
        '''Cartesian coordinates'''

        return self._master.coords


    @coords.setter
    def coords(self, val):
        '''Setter of cartesian coordinates'''

        self._master.setField(val, field='coords')


    @property
    def tags(self):
        '''Cartesian coordinates'''

        return self._master.tags


    @tags.setter
    def tags(self, val):
        '''Setter of cartesian coordinates'''

        self._master.setField(val, field='tags')


    @property
    def size(self):
        '''Size of the master array (e.g., the number of particles)'''

        return self._master.shape[0]


    # this is just an example of creating and resizing self._master
    @size.setter
    def size(self, val):
        '''Example setter of size'''

        # if _master exists
        try:
            self._master.expand(val)
        # create one if not
        except:
            # get the wanted dtype for self._master conveniently using the facility function
            # but you could create your own method
            dt = dl_py2f.utils.nputils.getDTypeFromObj(self)
            # we strongly recommend to use our type RecArray derived from numpy.recarray to create self._master 
            self._master = dl_py2f.utils.nputils.RecArray(shape=(val,), dtype=dt)


    # here is how we view the structured array (embedded in self._master) as a mask array
    @property
    def zmatrix(self):
        '''Internal coordinates (Z-matrix)'''

        from numpy import isfinite, ma, stack

        b = self._master.zmatrix.bond
        a = self._master.zmatrix.angle
        d = self._master.zmatrix.dihedral
        j = self._master.zmatrix.j
        k = self._master.zmatrix.k
        l = self._master.zmatrix.l

        # array of masks
        mask = stack([j==-1, ~(isfinite(b)),
                      k==-1, ~(isfinite(a)),
                      l==-1, ~(isfinite(d))],
                     axis=-1)

        # construct the masked array
        marray = self._master.zmatrix.view(ma.MaskedArray)

        # apply the masking rules
        for i in range(marray.mask.size):
            marray.mask[i] = tuple(mask[i])

        return marray


    @zmatrix.setter
    def zmatrix(self, val):
        '''Setter of zmatrix'''

        self._zmatrix = val


    def doSomething(self):
        ''''''

        print('\n >>> Example.doSomething() (Py)')





