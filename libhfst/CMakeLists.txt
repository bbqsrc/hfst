add_library(hfst SHARED)

if(NOT HAVE_DLFCN_H)
  message("Adding support for dlfcn")
  target_include_directories(hfst PRIVATE "${CMAKE_SOURCE_DIR}/back-ends/dlfcn")
endif()

add_subdirectory(src)

# link_directories(AFTER ${ICU_LIBRARIES})

# message(${ICU_INCLUDE_DIRS})