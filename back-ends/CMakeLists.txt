# SUBDIRS=dlfcn sfst
# if ! WANT_OPENFST_UPSTREAM
# SUBDIRS += openfst openfstwin
# endif
# if ! WANT_FOMA_UPSTREAM
# SUBDIRS += foma
# endif

# add_subdirectory(dlfcn)
add_subdirectory(openfst)
add_subdirectory(sfst)
add_subdirectory(foma)