cmake_minimum_required(VERSION 3.25)
project({{project}} CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(LEETCODE_LOCAL "Enable local tests and lint targets" ON)

add_library({{problem}} INTERFACE)
target_include_directories({{problem}} INTERFACE ${PROJECT_SOURCE_DIR}/include)

enable_testing()
add_subdirectory(test)

if (LEETCODE_LOCAL)
    file(GLOB_RECURSE LINT_SOURCES ${PROJECT_SOURCE_DIR}/include/*.hpp ${PROJECT_SOURCE_DIR}/test/*.cpp)
    add_custom_target(format COMMAND clang-format-20 -i ${LINT_SOURCES})
    add_custom_target(format-check COMMAND clang-format-20 --dry-run --Werror ${LINT_SOURCES})
    add_custom_target(tidy-check COMMAND clang-tidy-20 -p ${CMAKE_BINARY_DIR} ${PROJECT_SOURCE_DIR}/test/runner.cpp)
endif ()
