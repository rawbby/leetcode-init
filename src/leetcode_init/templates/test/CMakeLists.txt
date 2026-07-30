file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/case.hpp.in [=[#pragma once
#define CASE_INPUT R"__case__(@CASE_IN@)__case__"
#define CASE_EXPECTED R"__case__(@CASE_OUT@)__case__"
]=])

function(add_case name case_dir stem)
  file(READ ${case_dir}/${stem}.in CASE_IN)
  file(READ ${case_dir}/${stem}.out CASE_OUT)
  configure_file(${CMAKE_CURRENT_BINARY_DIR}/case.hpp.in cases/${name}.hpp @ONLY)
  add_executable(test_${name} runner.cpp)
  target_include_directories(test_${name} PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/cases)
  target_link_libraries(test_${name} PRIVATE {{problem}})
  target_compile_definitions(test_${name} PRIVATE CASE_HEADER="${name}.hpp")
  add_test(NAME ${name} COMMAND test_${name})
endfunction()

file(GLOB case_files CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/*.in)
foreach(f IN LISTS case_files)
  get_filename_component(stem ${f} NAME_WE)
  add_case(${stem} ${CMAKE_CURRENT_SOURCE_DIR} ${stem})
endforeach()

if(LEETCODE_LOCAL)
  file(GLOB case_files CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/local/*.in)
  foreach(f IN LISTS case_files)
    get_filename_component(stem ${f} NAME_WE)
    add_case(local_${stem} ${CMAKE_CURRENT_SOURCE_DIR}/local ${stem})
  endforeach()
endif()
