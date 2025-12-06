#include <iostream>
#include <fstream>
#include <string>

#include "bipartite_graph.hpp"
#include "max_independent_set.hpp"
#include "utils.hpp"

int main(int argc, char* argv[]) {
    BipartiteGraph g(0, 0);
    
    try {
        if (argc > 1) {
            // Read from file
            std::string filename = argv[1];
            g = readGraphFromFile(filename);
            std::cout << "Graph loaded from: " << filename << std::endl;
        } else {
            // Read from stdin
            g = readGraphFromInput(std::cin);
        }
        
        printGraphInfo(g);
        
        std::vector<int> mis = maximumIndependentSet(g);
        
        std::cout << "\\n=== Maximum Independent Set ===" << std::endl;
        printIndependentSet(mis, g.numU());
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
