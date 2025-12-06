#include <fstream>
#include <algorithm>

#include "utils.hpp"

BipartiteGraph readGraphFromInput(std::istream& in) {
    int nU, nW, m;
    
    in >> nU >> nW >> m;
    
    BipartiteGraph g(nU, nW);
    
    for (int i = 0; i < m; i++) {
        int u, w;
        in >> u >> w;
        g.addEdge(u, w);
    }
    
    return g;
}

BipartiteGraph readGraphFromFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filename);
    }
    return readGraphFromInput(file);
}

void printIndependentSet(const std::vector<int>& mis, int nU, std::ostream& out) {
    out << "Size: " << mis.size() << std::endl;
    out << "Vertices: ";
    
    for (size_t i = 0; i < mis.size(); i++) {
        if (i > 0) out << ", ";
        
        if (mis[i] < nU) {
            out << "U" << mis[i];
        } else {
            out << "W" << (mis[i] - nU);
        }
    }
    out << std::endl;
}

void printGraphInfo(const BipartiteGraph& g, std::ostream& out) {
    int totalEdges = 0;
    for (int u = 0; u < g.numU(); u++) {
        totalEdges += g.neighborsU(u).size();
    }
    
    out << "Graph Info:" << std::endl;
    out << "  U vertices: " << g.numU() << std::endl;
    out << "  W vertices: " << g.numW() << std::endl;
    out << "  Total vertices: " << (g.numU() + g.numW()) << std::endl;
    out << "  Edges: " << totalEdges << std::endl;
}