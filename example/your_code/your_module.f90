module yourModule

    implicit none

    private

    integer, parameter :: sp = selected_real_kind(6, 37)
    integer, parameter :: dp = selected_real_kind(15, 307)
    
    type type_01
        real(kind=8) :: rvar01 = 1.0
    endtype type_01
    type type_02
        integer         :: ivar01
        integer         :: ivar02
        integer(kind=8) :: ivar03 = 321
        real(kind=8)    :: rvar01
        integer         :: ivar04 = 1004
        type(type_01)   :: t1ar01(3)
        integer         :: ivar05 = 0
        integer         :: ivar06
    end type type_02
    type type_03
        real(kind=4)               :: rarr00(13)
        integer      , pointer     :: ivar00
        type(type_03), allocatable :: t3ar00(:)
        type(type_03), pointer     :: t3va00 !=> null() ! this is just for testing because it's very dangerous to use unnullified pointers (wild pointers), same below!
                                             ! DL_PY2F will issue a warning if debug=True
        integer                    :: ivar01
        type(type_02)              :: t2ar01(5)
        type(type_03), allocatable :: t3ar01(:,:)
        integer                    :: ivar02
        real(kind=8)               :: rarr01(3,4) = 3.4
        integer                    :: iarr01(2,3,4) = 234
        type(type_02), allocatable :: t2ar02(:)
        integer                    :: ivar03 = 1234567
        type(type_02), pointer     :: t2ar03(:,:,:,:) => null()
        character(len=25)          :: cvar01 = 'char 01'
        type(type_02), pointer     :: t2va01 => null()
        integer                    :: ivar04 = 444
        type(type_03), pointer     :: t3va01 => null()
        integer(kind=8)            :: ivar05 = 555
        integer, pointer           :: ivar06
        character(len=15)          :: cvar02 = 'char 02'
        type(type_02), pointer     :: t2va02(:)! => null() 
        integer(kind=8)            :: ivar07 = 777
        type(type_02)              :: t2va03
        integer(kind=8)            :: ivar08 = 888
        contains
            procedure, private :: procedure_xx
            procedure, private :: xx_int, xx_float
            generic  , public  :: xx => xx_int, xx_float
    !        procedure :: procedure_yy
    !        procedure :: procedure_xxx
    !        procedure, public :: xxx => xx_int, xx_float
    !        procedure :: procedure_yyy
    endtype type_03
    type type_04
        integer                           :: ivar01 = 101
        type(type_03)                     :: t3va01
        integer                           :: ivar02
        character(len=33)                 :: cvar01 = 'ABCDEFG'
        real(kind=8)     , allocatable    :: rarr01(:)
        integer                           :: ivar03 = 333333
        character(len=:) , allocatable    :: cvar02
        integer                           :: ivar04
        type(type_02)    , pointer        :: t2va01
        integer                           :: ivar05
        integer                           :: ivar06
        real(kind=8)     , pointer        :: rarr02(:)
        integer                           :: ivar07
        integer                           :: ivar08
        type(type_04)    , pointer        :: t4va01 ! here a unnullified pointer of linked list is super dangerous!
        integer                           :: ivar09
        real(kind=8)     , dimension(-4:9,2:19) :: rarr03 = 3D0 ! in Python we still index from 0
        integer                           :: ivar10
        integer                           :: ivar11
        character(len=:) , pointer        :: cvar03
        integer                           :: ivar12
        type(type_02)                     :: t2ar01(3,2)
        real(kind=8)                      :: rvar01 = 1.1111D0
        real(kind=8)                      :: rvar02
        real(kind=8)                      :: rvar03
        real(kind=8)                      :: rvar04
        logical                           :: lvar01
        type(type_02)    , pointer        :: t2ar02(:,:)
        logical                           :: lvar02 = .false.
        logical                           :: lvar03 = .true.
        integer                           :: ivar13
        integer                           :: ivar14
        character(len=13)                 :: carr01(25,21)
        real(kind=8)                      :: rvar05 = 0.98765
        logical                           :: lvar04
        integer                           :: ivar15 = 15
        logical                           :: lvar05
        real(kind=4)     , pointer        :: rvar06
        integer                           :: ivar16
        integer                           :: ivar17
        integer                           :: ivar18
        integer                           :: ivar19
        integer                           :: ivar20
        character(len=:) , pointer        :: carr02(:)
        integer                           :: ivar21
        real(kind=4)                      :: rvar07
        real(kind=8)                      :: rvar08
        logical                           :: lvar06
        integer                           :: ivar22
        real(kind=4)                      :: rvar09
        integer                           :: ivar23
        character(len=3) , dimension(4,5) :: carr03
        integer                           :: ivar24
        real(kind=8)                      :: rvar10
        real(kind=8)                      :: rvar11
        real(kind=8)     , allocatable    :: rarr04(:)
        real(kind=8)                      :: rvar12
        real(kind=4)                      :: rvar13
        integer                           :: ivar25
        real(kind=8)     , allocatable    :: rarr05(:,:)
        integer                           :: ivar26
        real(kind=8)                      :: rvar14
        integer                           :: ivar27
        integer                           :: ivar28
        real(kind=8)                      :: rvar15
        real(kind=8)                      :: rvar16
        integer                           :: ivar29
        integer                           :: ivar30
        real(kind=8)     , allocatable    :: rarr06(:,:,:)
        logical                           :: lvar07
        real(kind=8)                      :: rvar17
        integer                           :: ivar31
        integer                           :: ivar32
        integer                           :: ivar33
        real(kind=8)     , allocatable    :: rarr07(:,:)
        integer          , allocatable    :: iarr01(:)
        real(kind=8)     , allocatable    :: rarr08(:,:,:)
        logical                           :: lvar08
        integer                           :: ivar34
        real(kind=8)                      :: rvar18 = 18.0
        real(kind=8)     , allocatable    :: rarr09(:)
        real(kind=4)                      :: rvar19
        real(kind=4)                      :: rvar20
        real(kind=8)     , allocatable    :: rarr10(:)
        integer                           :: ivar35
        real(kind=8)                      :: rvar21
        integer                           :: ivar36
        real(kind=8)     , allocatable    :: rarr11(:)
        real(kind=8)     , allocatable    :: rarr12(:,:)
        integer                           :: ivar37 = 37
        logical          , pointer        :: lvar09
        integer                           :: ivar38
        integer                           :: ivar39
        integer                           :: ivar40
        integer                           :: ivar41
        real(kind=8)                      :: rvar22
        real(kind=8)                      :: rvar23
        real(kind=8)                      :: rvar24
        integer                           :: ivar42
        integer                           :: ivar43
        real(kind=8)     , allocatable    :: rarr13(:)
        integer                           :: ivar44
        integer                           :: ivar45
        real(kind=8)     , allocatable    :: rarr14(:,:,:)
        real(kind=8)                      :: rvar25
        real(kind=8)                      :: rvar26
        real(kind=8)     , allocatable    :: rarr15(:)
        real(kind=4)     , allocatable    :: rarr16(:,:,:)
        real(kind=8)     , allocatable    :: rarr17(:,:)
        real(kind=8)                      :: rvar27 = 2.7D0
        character(len=7) , allocatable    :: carr04(:)
        integer                           :: ivar46
        integer                           :: ivar47 = 47
        integer                           :: ivar48
        integer                           :: ivar49
        integer                           :: ivar50
        integer                           :: ivar51
        integer                           :: ivar52
        integer(kind=8)                   :: ivar53 = 53
        logical                           :: larr1(15) = .true.
        real(kind=8)     , allocatable    :: rarr18(:)
        integer                           :: iarr02(8,9,10) = 8910
        real(kind=8)                      :: rvar28
        integer                           :: iarr03(2,3)= reshape((/ 44,55,66,77,88,99 /), (/2,3/))
        real(kind=8)                      :: rvar29
        real(kind=8)                      :: rvar30
        real             , pointer        :: rarr19(:)
        type(type_03)    , allocatable    :: t3ar01(:)
        real(kind=8)                      :: rvar31 = 0.045D0
        type(type_03)                     :: t3ar02(3)
        real(kind=8)                      :: rvar32
        real(kind=8)                      :: rvar33
        real(kind=8)                      :: RVAR34
        real(kind=8)                      :: rvar35
        real(kind=8)                      :: rvar36
        real(kind=8)                      :: rvar37
        real(kind=8)                      :: rvar38 = 38D1
        integer          , allocatable    :: iarr04(:)
        integer(kind=8)  , allocatable    :: iarr05(:,:)
        integer          , allocatable    :: iarr06(:,:)
        real(kind=8)     , allocatable    :: rarr20(:)
        integer          , allocatable    :: iarr07(:)
        integer(kind=4)                   :: ivar54 = -54
        integer                           :: ivar55 = -5555
        logical                           :: lvar10
        real(kind=8)     , allocatable    :: rarr21(:)
    endtype type_04
    type type_00
        integer                           :: i1 = 100001
        type(type_04)                     :: t1
        integer                           :: i2
    endtype type_00

    real(kind=8)     , save      :: var01_of_real = 2.0251D3
    integer(kind=8)  , parameter :: arr01_of_int(4,6) = reshape((/  1, 2, 3, 4, &
                                                                    5, 6, 7, 8, &
                                                                    9,10,11,12, &
                                                                   13,14,15,16, &
                                                                   17,18,19,20, &
                                                                   21,22,23,24 /), (/4,6/))
    integer(kind=4)              :: arr02_of_int(5,3) = 1666
    type(type_04)                :: var_of_t04
    type(type_00)                :: var_of_t00
    real(kind=4)     , parameter :: var02_of_real = -12.3456789E-2
    logical          , parameter :: var01_of_logical = .true.
    character(len=15), parameter :: var01_of_char = 'Happy New Year!'
    real(kind=4)     , target    :: var03_of_real = 3.3333_sp
    real(kind=4)     , pointer   :: var04_of_real
    character(len=21)            :: arr01_of_char(3,4,5) = 'Hello, World!'
    character(len=5) , pointer   :: arr02_of_char(:)
    integer          , dimension(-3:5) :: arr03_of_int = (/-3,-2,-1,0,1,2,3,4,5/)

    public :: var_of_t04, var_of_t00
    public :: var01_of_real, var02_of_real, var03_of_real, var04_of_real
    public :: var01_of_logical, var01_of_char
    public :: arr01_of_int, arr02_of_int, arr03_of_int
    public :: arr01_of_char, arr02_of_char

    contains
        subroutine procedure_xx(self)
            class(type_03) :: self
        endsubroutine procedure_xx
        subroutine procedure_xxx(self)
            class(type_03) :: self
        endsubroutine procedure_xxx
        subroutine xx_int(self, i)
            class(type_03) :: self
            integer        :: i
        endsubroutine xx_int
        subroutine xx_float(self, f)
            class(type_03) :: self
            real(kind=4)   :: f
        endsubroutine xx_float
        subroutine procedure_yy(self)
            class(type_03) :: self
        endsubroutine procedure_yy
        subroutine procedure_yyy(self)
            class(type_03) :: self
        endsubroutine procedure_yyy

endmodule yourModule
