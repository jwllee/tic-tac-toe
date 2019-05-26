cmake_minimum_required (VERSION 3.5)
project (TicTacToe)

# the version number
set (TicTacToe_VERSION_MAJOR 1)
set (TicTacToe_VERSION_MINOR 0)

message ("Project source directory: ${PROJECT_SOURCE_DIR}")
message ("Project binary directory: ${PROJECT_BINARY_DIR}")

add_executable(Tutorial src/tutorial.cpp)
add_executable(PassByRef src/pass_by_ref.cpp)
