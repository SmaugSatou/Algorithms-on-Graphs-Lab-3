#pragma once

#include <vector>
#include <string>
#include <iostream>

#include "bipartite_graph.hpp"

// Input/Output functions

/** Read graph from input stream (format: nU nW m, then m edges as u w pairs). */
BipartiteGraph readGraphFromInput(std::istream& in = std::cin);

/** Read graph from file. */
BipartiteGraph readGraphFromFile(const std::string& filename);

/** Print independent set vertices (U vertices and W vertices are distinguished). */
void printIndependentSet(const std::vector<int>& mis, int nU, std::ostream& out = std::cout);

/** Print basic graph statistics. */
void printGraphInfo(const BipartiteGraph& g, std::ostream& out = std::cout);