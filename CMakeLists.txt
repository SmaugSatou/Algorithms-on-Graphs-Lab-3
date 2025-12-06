cmake_minimum_required(VERSION 3.10)
project(MinVertexCover)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

# Create library for bipartite graph operations
add_library(bipartite_graph_lib
    src/bipartite_graph.cpp
    src/max_independent_set.cpp
    src/utils.cpp
)

# Main executable
add_executable(min_vertex_cover
    main.cpp
)

target_link_libraries(min_vertex_cover bipartite_graph_lib)
