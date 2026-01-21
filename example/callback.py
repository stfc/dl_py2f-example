from . import example_dirs
from time import time

def callback(*args) -> int:
    '''Callback function for DL_FIND'''

    print('\n >>> Python: Callback:\n')

    ##################################################################
    # PART 1: we could do further computions/manipulations using the
    #         current callback function
    ##################################################################

    callback.obj.coords += 0.5
    print(" >>> callback (Py): coords =\n", callback.obj.coords)

    # we have to use a one-element array for a single value because Python's scalar
    # values such as a float is immutable
    # NB: do NOT use `callback.obj.energy = 9.9999` which redefines `callback.obj.energy`
    #     unless there is a proper setter function (paired with a @property decorator)
    callback.obj.energy[:] *= 9.9999
    print(" >>> callback (Py): energy =\n", callback.obj.energy)

    # we could even run more Python methods
    callback.obj.doSomething()

    ##################################################################
    # PART 2 (optional): Fortran-to-Python
    # NB: currently this only works with gfortran!
    ##################################################################
    # we could typically insert Pythonic interventions (for example a
    # machine-learned procedure)
    # of course this does not rely on the callback function and can be
    # applied outside here as an independent procedure
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # WARNING: this is a BETA version which must be used WITH CAUTION!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    from . import dl_py2f
    from os import path
    from ctypes import c_float, c_double, c_long

    libexample = dl_py2f.DL_DL(path.join(example_dirs.libdir, 'libexample.so'))

    # in case you want to find out all symbols in the shared library
    symbols = libexample.getModuleSymbols('yourmodule')
    unsupported = False
    print('\n Symbols exported from', path.join(example_dirs.libdir, 'libexample.so'))
    for symbol in symbols:
        print('    ', symbol, flush=True)
        if 'yourmodule_mp_procedure_xxx' in symbol or '_QMyourmodulePprocedure_xxx' in symbol:
            unsupported = True

    # currently only works with GNU
    if unsupported:
        print('\n Skipping Fortran-to-Python interoperability because we do not yet support it with Intel or Flang compilers...')
        return 0

    ##################################################################
    ### method A: implicit module parsing
    ##################################################################
    # below are some exemplar syntaxes which are pretty simple to use

    # define a directory where the Fortran module files are located
    libexample.moddir = example_dirs.moddir

    # retrieve the values as members of libexample.modules.yourmodule where "yourmodule" must be the module's name
    print()
    print(" >>> callback (Py): libexample.modules.yourmodule.var_of_t04.cvar01 =\n"+" "*19,
                               libexample.modules.yourmodule.var_of_t04.cvar01)
    # (this has automatically triggered parsing of all modules under example_dirs.moddir)

    # NB: we transpose the dimensions which are var_of_t04%iarr02(4,3,2) in Fortran
    print(" >>> callback (Py): libexample.modules.yourmodule.var_of_t04.iarr02[1,2,3] was\n"+" "*19,
                               libexample.modules.yourmodule.var_of_t04.iarr02[1,2,3])
    # we can change the values in an array which will be reflected in Fortran
    libexample.modules.yourmodule.var_of_t04.iarr02[1,2,3] = 123
    print(" >>> callback (Py): libexample.modules.yourmodule.var_of_t04.iarr02[1,2,3] now is\n"+" "*19,
                               libexample.modules.yourmodule.var_of_t04.iarr02[1,2,3])

    # scalar values likewise
    print(" >>> callback (Py): libexample.modules.yourmodule.var_of_t04.ivar37 was\n"+" "*19,
                               libexample.modules.yourmodule.var_of_t04.ivar37)
    libexample.modules.yourmodule.var_of_t04.ivar37 = 3377
    print(" >>> callback (Py): libexample.modules.yourmodule.var_of_t04.ivar37 now is\n"+" "*19,
                               libexample.modules.yourmodule.var_of_t04.ivar37)

    # WARNING: in this example, var03_of_real is a single-precision (32-bit or 4-byte) float in Fortran, however
    #          when we get the value in Python as c_float it's always converted to Python's <class 'float'>
    #          which is 64-bit [via 'c_float({!r})'.format(self.value)]
    print("\n >>> callback (Py): libexample.modules.yourmodule.var03_of_real was\n"+" "*19,
                                 libexample.modules.yourmodule.var03_of_real)
    # in this example, var04_of_real is a pointer to var03_of_real (see your_code.f90)
    libexample.modules.yourmodule.var04_of_real = 4.4444444444
    print(" >>> callback (Py): libexample.modules.yourmodule.var03_of_real now is\n"+" "*19,
                               libexample.modules.yourmodule.var03_of_real)
    libexample.modules.yourmodule.var03_of_real = 3.3333333333
    print(" >>> callback (Py): libexample.modules.yourmodule.var04_of_real =\n"+" "*19,
                               libexample.modules.yourmodule.var04_of_real)
    print(" >>> callback (Py): libexample.modules.yourmodule.var_of_t04.rvar06 =\n"+" "*19,
                               libexample.modules.yourmodule.var_of_t04.rvar06)
    # in Python we cannot use customised indices (l-/ubounds) as rarr03 is declared
    # `real(kind=8)     , dimension(-4:9,2:19) :: rarr03 = 3D0`
    print(" >>> callback (Py): libexample.modules.yourmodule.var_of_t04.rarr03.shape =\n"+" "*19,
                               libexample.modules.yourmodule.var_of_t04.rarr03.shape)
    # in Python we cannot use customised indices (l-/ubounds) as rarr03 is declared
    print(" >>> callback (Py): libexample.yourmodule.arr03_of_int =\n"+" "*19,
                               libexample.modules.yourmodule.arr03_of_int)

    # we return .value of a ctypes instance by default but we can change the behaviour
    libexample.return_ctype = True
    print(" >>> callback (Py): libexample.yourmodule.var_of_t04.rvar31 =\n"+" "*19,
                               libexample.modules.yourmodule.var_of_t04.rvar31)
    libexample.return_ctype = False

    # arr01_of_char(3,1,2) in Fortran
    print(" >>> callback (Py): libexample.modules.yourmodule.arr01_of_char[1,0,2] =\n"+" "*19,
                               libexample.modules.yourmodule.arr01_of_char[1,0,2])
    libexample.modules.yourmodule.arr01_of_char[1,0,2] = 'See you soon!'
    print(" >>> callback (Py): libexample.modules.yourmodule.arr01_of_char[1,0,2] =\n"+" "*19,
                               libexample.modules.yourmodule.arr01_of_char[1,0,2])


    arr02_of_char = libexample.getValue('arr02_of_char', str, (6,), module='yourmodule')

    ##################################################################
    ### method B: explicit module parsing ###
    ##################################################################
    # parse all module files under the given directory
    mods = libexample.parseAllModules(example_dirs.moddir, debug=False)
    print()
    print(" >>> callback (Py): mods.yourmodule.var02_of_real               =",
                               mods.yourmodule.var02_of_real)
    # the above call to parseAllModules() also made `libexample.modules` available
    print(" >>> callback (Py): libexample.modules.yourmodule.var02_of_real =",
                               libexample.modules.yourmodule.var02_of_real)
    # alternatively we can parse a specific Fortran module file
    your_mod = libexample.parseModule(path.join(example_dirs.moddir, 'yourmodule.mod'), debug=False)
    print(" >>> callback (Py): your_mod.var02_of_real                      =",
                               your_mod.var02_of_real)



    ##################################################################
    # module-level parameters (constants) that are not exported as
    # shared library symbols
    ##################################################################
    print(" >>> callback (Py): your_mod.var01_of_logical =", your_mod.var01_of_logical)
    print(" >>> callback (Py): your_mod.var01_of_char ="   , your_mod.var01_of_char)
    print(" >>> callback (Py): your_mod.arr01_of_real =\n" , your_mod.arr01_of_int)



    ##################################################################
    # module-level data directly exported to the shared library can be
    # accessed without parsing the modules
    ##################################################################
    # another method of retrieving an object is the getValue() function
    arr = libexample.getValue('arr02_of_int', int, (3,5), module='yourmodule')
    arr[0] = 1506
    print("\n >>> callback (Py): arr02_of_int =\n", arr)

    coords = libexample.getValue('coords', float, callback.obj.coords.shape, module='datamodule')
    print("\n >>> callback (Py): coords with implicit module parsing =\n", coords)



    ##################################################################
    # below are some data validations and more examples of the syntaxes
    ##################################################################

    # this is equivalent to `v0 = libexample.getValue('__yourmodule_MOD_var01_of_real', float)`
    # `float` here is equivalent to `ctypes.c_double`
    v0 = libexample.getValue('var01_of_real', float, module='yourmodule')
    # for testing the code only
    assert v0 == 2025.1, '\n >>> ERROR: var01_of_real should be 2025.1'
    # the setValue() function is the counterpart of getValue()
    # (we do not yet support a syntax such as 'var_of_t04%cvar01')
    libexample.setValue('var01_of_real', 3.14, module='yourmodule')
    v1 = libexample.getValue('var01_of_real', float, module='yourmodule')
    print(f'\n >>> callback (Py): var01_of_real set from {v0} to {v1}')

    # get the instance `var_of_t04` of the derived type `type_04`
    # NB: `return_ctype=False` is defaulted for convenience, otherwise all "dot" operators return ctypes
    #     instances (e.g., `c_long(15)` which needs `c_long(15).value` for comparing with `15`)
    var_of_t04 = libexample.getValue('var_of_t04', module='yourmodule', return_ctype=False, debug=False)

    # `var_of_t04.cvar01` is equivalent to `libexample.getValue('var_of_t04%cvar01', module='yourmodule')`
    v0 = var_of_t04.cvar01
    # for testing the code only
    assert v0.strip() == 'ABCDEFG', '\n >>> ERROR: var_of_t04.cvar01 should be "ABCDEFG"'
    var_of_t04.cvar01 = 'dl_py2f'
    print(f' >>> callback (Py): var_of_t04.cvar01 set from "{v0}" to "{var_of_t04.cvar01}"')

    # `return_ctype=False` is defaulted for convenience, while a ctypes instance (`c_long(15)`
    # instead of `15`) is returned if `return_ctype=True` is specified
    v0 = libexample.getValue('var_of_t04%ivar15', module='yourmodule', return_ctype=True, debug=False)
    # for testing the code only
    assert v0.value == 15, '\n >>> ERROR: var_of_t04.ivar15 should be 15'
    print(f' >>> callback (Py): var_of_t04.ivar15 set from {v0}', end='')
    var_of_t04.ivar15 = 150
    print(f' to {var_of_t04.ivar15}')

    # this is equivalent to `var_of_t04.t2ar02[3,4].t1ar01[1].rvar01`
    # NB: Python is row-major (like C) cf. Fortran (column-major) so that
    #     we transpose the dimensions
    # NB: Python counts from 0 while Fortran from 1
    v0 = libexample.getValue('var_of_t04%t2ar02(5,4)%t1ar01(2)%rvar01', module='yourmodule', debug=False)
    # for testing the code only
    assert v0 == 1.0, '\n >>> ERROR: var_of_t04.t2ar02[3,4].t1ar01[1].rvar01 should be 1.0'
    print(f' >>> callback (Py): var_of_t04.t2ar02[3,4].t1ar01[1].rvar01 set from {v0}', end='')
    var_of_t04.t2ar02[3,4].t1ar01[1].rvar01 = 3.41
    print(f' to {var_of_t04.t2ar02[3,4].t1ar01[1].rvar01}')

    # this is equivalent to `libexample.getValue('var_of_t04%t2ar02(4,3)%ivar04', module='yourmodule')`
    v0 = var_of_t04.t2ar02[2,3].ivar04
    # for testing the code only
    assert v0 == 1004, '\n >>> ERROR: var_of_t04.t2ar02[2,3].ivar04 should be 1004'
    print(f' >>> callback (Py): var_of_t04.t2ar02[2,3].ivar04 set from {v0}', end='')
    var_of_t04.t2ar02[2,3].ivar04 = 2025
    print(f' to {var_of_t04.t2ar02[2,3].ivar04}')

    # this is equivalent to `libexample.getValue('var_of_t04%t3ar01(3)%ivar07', module='yourmodule')`
    v0 = var_of_t04.t3ar01[2].ivar07
    # for testing the code only
    assert v0 == 777, '\n >>> ERROR: var_of_t04.t3ar01[2].ivar07 should be 777'
    print(f' >>> callback (Py): var_of_t04.t3ar01[2].ivar07 set from {v0}', end='')
    var_of_t04.t3ar01[2].ivar07 = 2014
    print(f' to {var_of_t04.t3ar01[2].ivar07}')

    # and more exemplar calculations which will be reflected on the Fortran side
    for i in range(len(var_of_t04.rarr21)):
        var_of_t04.rarr21[i] = float(i+1)


    # we support PDE-style slicing
    print("\n >>> callback (Py): scanning along var_of_t04.t2ar02[:,2], ivar04 =")
    for a in var_of_t04.t2ar02[:,2]:
        print(a.ivar04, end=' ')
    print("\n >>> callback (Py): scanning along var_of_t04.t2ar02[1:5,:], ivar04 =")
    for a in var_of_t04.t2ar02[1:5,:]:
        print(a.ivar04, end=' ')
    print("\n >>> callback (Py): scanning along var_of_t04.t2ar02[::2,::2], ivar04 =")
    for a in var_of_t04.t2ar02[::2,::2]:
        print(a.ivar04, end=' ')
    print("\n >>> callback (Py): scanning along var_of_t04.t2ar02[...,1], ivar04 =")
    for a in var_of_t04.t2ar02[...,1]:
        print(a.ivar04, end=' ')
    print("\n >>> callback (Py): scanning along var_of_t04.t2ar02[1,:,2], ivar04 =")
    print("\n >>> callback (Py): scanning along var_of_t04.t2ar02[-2:-1,:-2], ivar04 =")
    for a in var_of_t04.t2ar02[-2:-1,-2]:
        print(a.ivar04, end=' ')
    print("\n >>> callback (Py): scanning along var_of_t04.t2ar02[::-1,0], ivar04 =")
    for a in var_of_t04.t2ar02[::-1,0]:
        print(a.ivar04, end=' ')
    print("\n >>> callback (Py): shape of var_of_t04.t2ar02[:,None,:] =")
    print(var_of_t04.t2ar02[:,None,:].shape)
    print('', flush=True)

    return 0
