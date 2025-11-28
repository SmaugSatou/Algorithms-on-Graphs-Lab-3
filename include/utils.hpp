#pragma once

#include "bipartite_graph.hpp"

BipartiteGraph readGraphFromInput();
void printIndependentSet(const std::vector<int>& set, bool isUSet, int size);