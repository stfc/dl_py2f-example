function do_something_externally() result(ierror)

    use ExampleModule, only : PyCallback, PyObj
    use DataModule   , only : coords, energy

    implicit none

    integer               :: ierror
    real(kind=8), pointer :: onedimdbl(:)

    ! map the changes in the main routine (Fortran) back to Python
    call PyObj%set('coords', coords)
    call PyObj%set('energy', (/ energy /))

    allocate(onedimdbl(1))
    call PyObj%get('energy', onedimdbl)

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

    deallocate(onedimdbl)

endfunction do_something_externally
integer function get_coords() result(ierror)

    use ExampleModule, only : PyObj
    use DataModule   , only : coords

    implicit none

    integer nparticles

    call PyObj%get('size', nparticles)
    allocate(coords(3,nparticles))
    call PyObj%get('coords', coords)

endfunction get_coords
