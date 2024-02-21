# SUBDIRS=dlfcn sfst
# if ! WANT_OPENFST_UPSTREAM
# SUBDIRS += openfst openfstwin
# endif
# if ! WANT_FOMA_UPSTREAM
# SUBDIRS += foma
# endif

# add_subdirectory(dlfcn)
add_subdirectory(openfst)

if(HAVE_SFST)
    add_subdirectory(sfst)
endif()
add_subdirectory(foma)