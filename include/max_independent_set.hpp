#pragma once

#include <vector>

#include "bipartite_graph.hpp"

std::vector<int> maximumIndependentSet(const BipartiteGraph& g, bool& isUSet, int& size);