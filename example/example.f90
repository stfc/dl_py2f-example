module ExampleModule

    use, intrinsic :: iso_c_binding
    use DL_PY2F, only : dictType, PyType, ptr2dict

    private
    public interface_example, PyCallback, PyObj

    abstract interface
        integer(c_long) function callback() bind(c)
            use iso_c_binding
        endfunction callback
    endinterface

    procedure(callback), pointer :: PyCallback
    type(dictType)     , pointer :: PyObj
    contains

    function interface_example(objPtr) bind(c) result(ierror)

        implicit none

        type(PyType)   , intent(in) :: objPtr

        integer(c_int)              :: ierror
        integer                     :: i, m, nparticles, ierror_main
        real(kind=8)   , pointer    :: onedimdbl(:), twodimdbl(:,:), bond(:), angle(:), dihedral(:)
        integer(kind=4), pointer    :: f(:,:)
        integer(kind=8), pointer    :: c(:), j(:), k(:), l(:), tags(:)
        type(c_funptr)              :: pyfuncPtr
        integer        , external   :: main_of_your_code

        ! initialise PyObj
        allocate(PyObj, source=ptr2dict(objPtr))

        ! initialise the Python callback function
        call PyObj%get('callback', pyfuncPtr)
        call c_f_procpointer(pyfuncPtr, PyCallback)

        call PyObj%get('size', nparticles)
        print *
        print *, "interface_example (F): nparticles =", nparticles

        ! testing 1D 64-bit integer array (my_example.c in Python)
        call PyObj%get('c', c, readonly=.false.)
        ! by default, readonly=.false., otherwise change to the values will not reflect on the Python side
        c(1) = 2711
        print *
        print *, "interface_example (F): 1D array c of long integers ="
        print *, c

        ! testing 2D 32-bit integer array (my_example.f in Python)
        call PyObj%get('f', f)
        print *
        print *, "interface_example (F): 2D array f of integers ="
        do m = 1, 9
            print '(1x,a,i1,a,5i9)', "f(", m, ",:) =", f(m,:)
        enddo

        ! this is how we map a Python NumPy array to a Fortran one (pointer only without making a copy)
        ! allocate(twodimdbl(3,nparticles)) is unnecessary though harmless
        call PyObj%get('coords', twodimdbl, readonly=.true.)
        ! as readonly=.true., the change to the value does not affect the Python side
        twodimdbl(2,1) = -0.5
        flush(6)

#ifdef __NVCOMPILER
        ! here is a workaround for nvfortran due to a compiler bug with non-contiguous pointer arrays of intent(out):
        ! use readonly=.true. ("safe mode") to force a copy
        call PyObj%get('tags', tags, readonly=.true.)
        tags = tags + 100            ! 0,1,2,... -> 100,101,102,...
        call PyObj%set('tags', tags) ! write back to Python
#else
        ! gfortran/ifort/ifx/flang: with direct read/write access that changes values on the Python side
        call PyObj%get('tags', tags)
        tags = tags + 100
#endif

        print *
        print *, "interface_example (F): coords and tags ="
        do i = 1, nparticles
            print *, "X =", twodimdbl(1,i), " Y =", twodimdbl(2,i), " Z =", twodimdbl(3,i), " tag =", tags(i)
        enddo

        ! this is how we map an embedded Python NumPy mask array to a Fortran one
#ifdef __NVCOMPILER
        ! nvfortran workaround: must use readonly=.true.
        call PyObj%get('j', j, readonly=.true.)
        call PyObj%get('k', k, readonly=.true.)
        call PyObj%get('l', l, readonly=.true.)
        call PyObj%get('bond', bond, readonly=.true.)
        call PyObj%get('angle', angle, readonly=.true.)
        call PyObj%get('dihedral', dihedral, readonly=.true.)
#else
        ! gfortran/ifort/ifx/flang: direct read/write access
        call PyObj%get('j', j)
        call PyObj%get('k', k)
        call PyObj%get('l', l)
        call PyObj%get('bond', bond)
        call PyObj%get('angle', angle)
        call PyObj%get('dihedral', dihedral)
#endif

        print *
        print *, "interface_example (F): part of zmatrix ="
        flush(6)
        print *, "   I       J    Bond    K   Angle    L  Dihedral"
        do i = 1, nparticles
            print '(1x,i4,4x,i4,f9.3,i4,f9.3,i4,f9.3)', i, j(i), bond(i), k(i), angle(i), l(i), dihedral(i)
        enddo 

        print *
        print *, "interface_example (F): calling to the main subroutine of your code (Fortran)..."
        ierror_main = main_of_your_code()

#ifdef __NVCOMPILER
        ! nvfortran workaround: must use readonly=.true.
        call PyObj%get('angle', onedimdbl, readonly=.true.)
        onedimdbl = 120.0                  ! set angles to 120.0
        call PyObj%set('angle', onedimdbl) ! write back to Python
#else
        ! gfortran/ifort/ifx/flang: direct read/write access
        call PyObj%get('angle', onedimdbl)
        onedimdbl = 120.0
#endif
        ! this is equivalent, especially useful when readonly=.true. above:
!        call PyObj%set('angle', onedimdbl)

        call PyObj%get('coords', twodimdbl)
        print *, "interface_example (F): final coords ="
        do i = 1, nparticles
            print *, " X =", twodimdbl(1,i), " Y =", twodimdbl(2,i), " Z =", twodimdbl(3,i)
        enddo 

        ! destroy PyObj after use
        call PyObj%finalise()

        ! beware that even after PyObj is destroyed twodimdbl still points to the original NumPy array (unless readonly=.true.)!
        twodimdbl(1,1) = -999.9999999

        deallocate(PyObj)

        ! unless readonly=.true. was used, we can only nullify but NOT deallocate these pointers because they do not own the Python data/procedures!
        nullify(PyCallback)
        nullify(onedimdbl, twodimdbl)
        nullify(c, f, j, k, l, tags)

        ierror = ierror_main

    endfunction interface_example

endmodule ExampleModule

