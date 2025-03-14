subroutine main_of_your_code()

    use yourModule, only : var_of_t00, var_of_t04, var01_of_real,    &
                           arr01_of_int, arr02_of_int, arr03_of_int, &
                           arr01_of_char, arr02_of_char,             &
                           var03_of_real, var04_of_real
    use dataModule, only : coords, energy

    implicit none

    integer                     :: i, j, ierror
    integer     , external      :: do_something_externally
    integer     , external      :: get_coords

    print *
    print *, "###################################"
    print *, "### main of your_code (Fortran) ###"
    print *, "###################################"
    print *

    print *
    print *, "main (F): arr01_of_int ="
    ! Fortran is column-major (rightmost indexing)
    do i = 1, 4
        print *, "    ", arr01_of_int(i,:)
    enddo

    var04_of_real => var03_of_real
    allocate(var_of_t04%t4va01)
    allocate(var_of_t04%t4va01%t4va01)
    allocate(var_of_t04%t2ar02(5,6))
    allocate(var_of_t04%t3ar01(56))
    allocate(var_of_t04%rarr21(12002))
    allocate(arr02_of_char(6))
    arr02_of_char = 'arr02_of_char'
    print *, "### loc of arr02_of_char =", loc(arr02_of_char)
    print *, "### loc of arr02_of_char(2) =", loc(arr02_of_char(2)) - loc(arr02_of_char)
    print *, "### loc of arr02_of_char(3) =", loc(arr02_of_char(3)) - loc(arr02_of_char(2))
    print *, "### shape of arr03_of_int =", shape(arr03_of_int)
    print *, "### shape of rarr03 =", shape(var_of_t04%rarr03)

    var_of_t04%rvar06 => var03_of_real

    ! initialise data by mapping to the Python arrays: no copies
    ! of arrays are made but only pointers are used
    ierror = get_coords()
    

    ! exemplar computations or manipulations on the passed-in data
    print *, "main (F): doing your own computions in Fortran..."
    coords = coords + 0.25
    energy = sum(coords)
    ! end of computations


    ! optional: here is how we call a Python callback function
    print *
    print *, "main (F): calling to the subroutine do_something_externally()..."
    ierror = do_something_externally()

    print *
    print *, "main (F): var01_of_real of module yourModule =", var01_of_real
    if(var01_of_real.ne.3.14D0) then
        print *, "          which should be 3.14"
        ierror = 1
    endif
    print *, "main (F): var_of_t04%cvar01 =", var_of_t04%cvar01
    if(trim(var_of_t04%cvar01).ne."dl_py2f") then
        print *, "          which should be dl_py2f"
        ierror = 1
    endif
    print *, "main (F): var_of_t04%t2ar02(4,3)%ivar04 =", var_of_t04%t2ar02(4,3)%ivar04
    if(var_of_t04%t2ar02(4,3)%ivar04.ne.2025) then
        print *, "          which should be 2025"
        ierror = 1
    endif
    print *, "main (F): var_of_t04%t3ar01(3).ivar07 =", var_of_t04%t3ar01(3)%ivar07
    if(var_of_t04%t3ar01(3)%ivar07.ne.2014) then
        print *, "          which should be 2014"
        ierror = 1
    endif
    print *, "main (F): var_of_t04%iarr02(4,3,2) =", var_of_t04%iarr02(4,3,2)
    if(var_of_t04%iarr02(4,3,2).ne.123) then
        print *, "          which should be 123"
        ierror = 1
    endif
    print *, "main (F): var_of_t04%ivar37 =", var_of_t04%ivar37
    if(var_of_t04%ivar37.ne.3377) then
        print *, "          which should be 3377"
        ierror = 1
    endif
    print *, "main (F): var_of_t04%rarr21(33) =", var_of_t04%rarr21(33)
    if(var_of_t04%rarr21(33).ne.33.0) then
        print *, "          which should be 33.0"
        ierror = 1
    endif
    ! NB: trim(arr01_of_char(3,1,2)) or trim(adjustl(...)) doesn't work here!
    print *, "main (F): arr01_of_char(3,1,2) =", arr01_of_char(3,1,2)
    if(arr01_of_char(3,1,2)(1:13).ne."See you soon!") then
        print *, "          which should be 'See you soon!'"
        ierror = 1
    endif

    print *
    print *, "#############################"
    print *, "### end of main (Fortran) ###"
    print *, "#############################"
    print *

    deallocate(var_of_t04%t2ar02)
    deallocate(var_of_t04%t3ar01)
    deallocate(var_of_t04%rarr21)
    deallocate(var_of_t04%t4va01)
    deallocate(coords)
    deallocate(arr02_of_char)

endsubroutine main_of_your_code
