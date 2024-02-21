# file(GLOB_RECURSE SOURCES "*.cc")
# file(GLOB_RECURSE INCLUDES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "*.h")

target_compile_options(hfst PRIVATE
    "-Wno-deprecated" "-Wall" "-Wextra"
    "-Wno-unused-parameter" "-Wno-sign-compare" "-g"
    "-I."
    "-I${PROJECT_SOURCE_DIR}/libhfst/src"
    "-I${PROJECT_SOURCE_DIR}/back-ends")

# message(${INCLUDES})

# message(${ICU_LIBRARIES})

target_include_directories(hfst PUBLIC
    ${ICU_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR})
    # "${CMAKE_SOURCE_DIR}/back-ends/foma"
    # "${CMAKE_SOURCE_DIR}/back-ends/openfst/src/include")

find_library(UC icuuc)
find_library(I18N icui18n)
find_library(DATA icudata)
# target_include_directories(hfst PRIVATE ${INCLUDES})
# target_sources(hfst PRIVATE ${SOURCES})

add_subdirectory(parsers)
add_subdirectory(implementations)
target_sources(hfst PRIVATE
    HfstApply.cc HfstInputStream.cc HfstTransducer.cc HfstOutputStream.cc
    HfstRules.cc HfstXeroxRules.cc HfstDataTypes.cc
    HfstSymbolDefs.cc HfstTokenizer.cc
    HfstFlagDiacritics.cc HfstExceptionDefs.cc
    HarmonizeUnknownAndIdentitySymbols.cc
    HfstLookupFlagDiacritics.cc
    HfstEpsilonHandler.cc HfstStrings2FstTokenizer.cc
    HfstPrintDot.cc HfstPrintPCKimmo.cc hfst-string-conversions.cc
    string-utils.cc
)
target_link_libraries(hfst PRIVATE ${UC} ${I18N} ${DATA} parsers)
target_link_libraries(hfst PUBLIC openfst foma sfst)
target_compile_options(hfst PUBLIC ${ICU_CFLAGS_OTHER})

