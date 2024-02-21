
if(NOT HAVE_DLFCN_H)
  add_subdirectory(dlfcn)
  include_directories("${CMAKE_SOURCE_DIR}/back-ends/dlfcn")
endif()

if(HAVE_OPENFST)
    add_subdirectory(openfst)
    if(WIN32)
        add_subdirectory(openfst)
    else()
        add_subdirectory(openfstwin)
    endif()
endif()

if(HAVE_SFST)
    add_subdirectory(sfst)
endif()

if(HAVE_FOMA)
    add_subdirectory(foma)
endif()
