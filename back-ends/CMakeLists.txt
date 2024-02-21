if(HAVE_OPENFST)
    add_subdirectory(openfst)
endif()

if(HAVE_SFST)
    add_subdirectory(sfst)
endif()

if(HAVE_FOMA)
    add_subdirectory(foma)
endif()