cmake_minimum_required(VERSION 3.5)
project (TicTacToe)

set(PROJECT_SOURCE_DIR "../src")

add_library(Catch INTERFACE)
target_include_directories(Catch INTERFACE catch)

include_directories(${PROJECT_SOURCE_DIR})
link_directories(${PROJECT_SOURCE_DIR})
add_subdirectory(${PROJECT_SOURCE_DIR})

add_executable(test-cell test_cell.cpp)
target_link_libraries(test-cell Cell Catch)

enable_testing()
add_test(NAME Cell-Test COMMAND test-cell)
