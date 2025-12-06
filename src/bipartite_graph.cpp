#include "bipartite_graph.hpp"

BipartiteGraph::BipartiteGraph(int nU, int nW) : nU_(nU), nW_(nW) {
    adjU_.resize(nU);
    adjW_.resize(nW);
}

void BipartiteGraph::addEdge(int u, int w) {
    adjU_[u].push_back(w);
    adjW_[w].push_back(u);
}

int BipartiteGraph::numU() const {
    return nU_;
}

int BipartiteGraph::numW() const {
    return nW_;
}

const std::vector<int>& BipartiteGraph::neighborsU(int u) const {
    return adjU_[u];
}

const std::vector<int>& BipartiteGraph::neighborsW(int w) const {
    return adjW_[w];
}
