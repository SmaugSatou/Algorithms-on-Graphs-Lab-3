#pragma once

#include <vector>
#include <utility>

/**
 * Bipartite graph representation with two vertex sets U and W.
 */
class BipartiteGraph {
private:
    int nU_, nW_;

    std::vector<std::vector<int>> adjU_;  // Adjacency list for U vertices
    std::vector<std::vector<int>> adjW_;  // Adjacency list for W vertices

public:
    /**
     * Construct a bipartite graph with nU vertices in U and nW vertices in W.
     */
    BipartiteGraph(int nU, int nW);

    /**
     * Add an edge between vertex u from U and vertex w from W.
     */
    void addEdge(int u, int w);

    /**
     * Get the number of vertices in set U.
     */
    int numU() const;

    /**
     * Get the number of vertices in set W.
     */
    int numW() const;

    /**
     * Get neighbors of vertex u from set U (returns vertices in W).
     */
    const std::vector<int>& neighborsU(int u) const;

    /**
     * Get neighbors of vertex w from set W (returns vertices in U).
     */
    const std::vector<int>& neighborsW(int w) const;
};