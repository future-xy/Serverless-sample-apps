cmake_minimum_required(VERSION 3.18)
project(cpp-inference)

find_package(Torch REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

add_executable(inference inference.cpp)
target_link_libraries(inference "${TORCH_LIBRARIES}")
set_property(TARGET inference PROPERTY CXX_STANDARD 14)