project(hfst)
cmake_minimum_required(VERSION 3.25)

if(APPLE)
    list(APPEND CMAKE_PREFIX_PATH /opt/homebrew)
    set(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} /opt/homebrew/lib)
    set(ENV{PKG_CONFIG_PATH} "/opt/homebrew/lib/pkgconfig")
endif()

set(CMAKE_CXX_FLAGS "-std=c++14 -w -DHAVE_CONFIG_H -I${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CXX_FLAGS}")
set(CMAKE_C_FLAGS "-w -DHAVE_CONFIG_H -I${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_C_FLAGS}")
find_package(PkgConfig)

# find_package(ICU REQUIRED uc)

include_directories(ICU_INCLUDE_DIRS)
pkg_check_modules(ICU icu-uc)

add_subdirectory(back-ends)
add_subdirectory(libhfst)
# add_subdirectory(tools)
# add_subdirectory(test)
# add_subdirectory(doc)
# add_subdirectory(man)
# add_subdirectory(scripts)