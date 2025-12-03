function do_something_externally() result(ierror)

    use ExampleModule, only : PyCallback, PyObj
    use DataModule   , only : coords, energy

    implicit none

    integer(kind=8)          :: ierror
    real(kind=8)   , pointer :: onedimdbl(:)

    ! map the changes in the main routine (Fortran) back to Python
    call PyObj%set('coords', coords)
    ! float is immutable in Python therefore we use an array of a single element
    call PyObj%set('energy', (/ energy /))

    ! the best way here to alter a float or an interger scalar value in Python is using it as an array
    ! (of a single element) because it is *immutable* in Python, though it still can be done in C (see
    ! the Fortran-to-Python interoperability)
    allocate(onedimdbl(1))
    call PyObj%get('energy', onedimdbl, readonly=.true.)
    ! this takes no effect on the Python side because readonly=.true.
    onedimdbl = onedimdbl*1.5
    ! in this case the Python value can only be change by the setter function
    call PyObj%set('energy', onedimdbl)

    print *
    print *, "do_something_externally (F): energy before callback =", onedimdbl

    print *
    print *, "do_something_externally (F): calling to the Python callback function..."
    ierror = PyCallback()

    ! to reflect the changes made in the callback function (Python) we must run the get() method again
    call PyObj%get('coords', coords)

    if(ierror.ne.0) then
        ! raise an error or so
    endif

    ! we have to use an array to change because scalar objects in Python such as a float is immutable
    call PyObj%get('energy', onedimdbl)
    print *
    print *, "do_something_externally (F): energy after callback =", onedimdbl

    ! do NOT deallocate because the pointer onedimdbl does not own the NumPy data
    nullify(onedimdbl)

endfunction do_something_externally
! this is how the original project retrieves data from the current extension
integer function get_coords() result(ierror)

    use ExampleModule, only : PyObj
    use DataModule   , only : coords

    implicit none

    call PyObj%get('coords', coords)

    ierror = 0

endfunction get_coords
