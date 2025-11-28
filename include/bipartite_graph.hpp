#pragma once

#include <vector>
#include <utility>

class BipartiteGraph {
private:
    int nU_, nW_;

    std::vector<std::vector<int>> adjU_;
    std::vector<std::vector<int>> adjW_;

public:
    BipartiteGraph(int nU, int nW);

    void addEdge(int u, int w);

    int numU() const;
    int numW() const;

    const std::vector<int>& neighborsU(int u) const;
    const std::vector<int>& neighborsW(int w) const;
};