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
        integer                     :: i, nparticles
        real(kind=8)   , pointer    :: twodimdbl(:,:)
        integer(kind=8), pointer    :: j(:), k(:), l(:), tags(:)
        real(kind=8)                :: energy(1)
        type(c_funptr)              :: pyfuncPtr

        ! initialise PyObj
        allocate(PyObj, source=ptr2dict(objPtr))

        ! initialise the Python callback function
        call PyObj%get('callback', pyfuncPtr)
        call c_f_procpointer(pyfuncPtr, PyCallback)

        call PyObj%get('size', nparticles)
        print *
        print *, "interface_example (F): nparticles =", nparticles

        ! this is how we map a Python NumPy array to a Fortran one (pointer only without making a copy)
        allocate(twodimdbl(3,nparticles))
        call PyObj%get('coords', twodimdbl)

        allocate(tags(nparticles))
        call PyObj%get('tags', tags)

        print *
        print *, "interface_example (F): coords and tags ="
        do i = 1, nparticles
            print *, "X =", twodimdbl(1,i), " Y =", twodimdbl(2,i), " Z =", twodimdbl(3,i), " tag =", tags(i)
        enddo 

        ! this is how we map an embedded Python NumPy mask array to a Fortran one (pointer only without making a copy)
        allocate(j(nparticles))
        allocate(k(nparticles))
        allocate(l(nparticles))
        call PyObj%get('j', j)
        call PyObj%get('k', k)
        call PyObj%get('l', l)
        print *
        print *, "interface_example (F): part of zmatrix ="
        do i = 1, nparticles
            print *, "J =", j(i), " K =", k(i), " L =", l(i)
        enddo 

        print *
        print *, "interface_example (F): calling to the main subroutine of your code (Fortran)..."
        call main_of_your_code

        call PyObj%get('coords', twodimdbl)
        print *, "interface_example (F): final coords ="
        do i = 1, nparticles
            print *, " X =", twodimdbl(1,i), " Y =", twodimdbl(2,i), " Z =", twodimdbl(3,i)
        enddo 

        deallocate(PyObj, twodimdbl, j, k, l)

        ierror = 0

    endfunction interface_example

endmodule ExampleModule

