cmake_minimum_required(VERSION 3.12)

project(My_Code
        VERSION       1.0
        DESCRIPTION  "An example source package using DL_PY2F"
        HOMEPAGE_URL "www.gitlab.com"
        LANGUAGES     Fortran)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib)
set(CMAKE_Fortran_MODULE_DIRECTORY ${PROJECT_BINARY_DIR}/modules)

# for convenience we make the paths to directories dynamic to be used in Python
configure_file(example_dirs.py.in ${PROJECT_SOURCE_DIR}/example_dirs.py @ONLY)

add_library(example SHARED example.f90
                           do_something_externally.f90
                           your_code/your_code.f90
                           your_code/your_module.f90
                           your_code/data_module.f90)

# compile DL_PY2F from source
if(FROM_SOURCE)
    add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/dl_py2f)
    include_directories(${PROJECT_BINARY_DIR}/dl_py2f/modules)
# use the system DL_PY2F: on Debian-type system only (installed via apt)
else()
    link_directories(/lib/x86_64-linux-gnu)
    #set_target_properties(example PROPERTIES LINK_FLAGS "-L/lib/x86_64-linux-gnu -ldl_py2f")
    include_directories(/usr/include/x86_64-linux-gnu)
endif()

target_link_libraries(example dl_py2f)


# either 32- or 64-bit integers (without or with -fdefault-integer-8 for GNU) should work for the Fortran->Python interoperability
if("${CMAKE_Fortran_COMPILER_ID}" STREQUAL GNU)
    # use of -fdefault-integer-8 must be in line with DL_PY2F
#    set_target_properties(example PROPERTIES COMPILE_FLAGS "-O2 -fPIC -fdefault-integer-8")
    set_target_properties(example PROPERTIES COMPILE_FLAGS "-O2 -fPIC")
    set_target_properties(dl_py2f PROPERTIES COMPILE_FLAGS "-O2 -fPIC")
elseif("${CMAKE_Fortran_COMPILER_ID}" STREQUAL IntelLLVM OR "CMAKE_Fortran_COMPILER_ID" STREQUAL Intel)
    # use of -i8 must be in line with DL_PY2F
    set_target_properties(example PROPERTIES COMPILE_FLAGS "-O2 -fPIC")
    set_target_properties(dl_py2f PROPERTIES COMPILE_FLAGS "-O2 -fPIC")
else()
    message(" WARNING: Unknown CMAKE_FORTRAN_COMPILER_ID!")
endif()


include(${CMAKE_CURRENT_LIST_DIR}/clean.cmake)

# above we compile all source files into a single shared library but in reality we could
# compile your code, which may be large-scale, as a static library (i.e. an archive)
# with -fPIC (you may use CMake's ExternalProject) and include it in the current dynamic
# library (a CMake object without your code), for example:
#add_library(example SHARED example.f90
#                           do_something_externally.f90)
#set_target_properties(example PROPERTIES LINK_FLAGS "-Wl,--whole-archive             \
#                                                     ${YOUR_CODE_DIR}/libyour_code.a \
#                                                     -Wl,--no-whole-archive          \
#                                                     -Wl,--version-script=${CMAKE_CURRENT_LIST_DIR}/export.map")
# hint: use a version script to control symbols to export and prevent name clashing



