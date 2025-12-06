#pragma once

#include <vector>

#include "bipartite_graph.hpp"

/**
 * Find the maximum independent set in a bipartite graph.
 * 
 * Uses König's theorem: |MIS| = |V| - |MaxMatching|
 * Implements Hopcroft-Karp algorithm to find maximum matching,
 * then constructs the MIS from the minimum vertex cover.
 * 
 * @param g The bipartite graph
 * @return Vector of vertex indices (U vertices: [0, nU), W vertices: [nU, nU+nW))
 */
std::vector<int> maximumIndependentSet(const BipartiteGraph& g);