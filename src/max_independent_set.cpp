#include <queue>
#include <algorithm>
#include <limits>

#include "max_independent_set.hpp"

namespace {

const int NIL = -1;
const int INF = std::numeric_limits<int>::max();

// BFS to find augmenting paths and compute levels
bool bfs(const BipartiteGraph& g, 
         std::vector<int>& pairU, 
         std::vector<int>& pairW, 
         std::vector<int>& dist) {
    std::queue<int> q;
    
    // Initialize distances and queue all unmatched vertices from U
    for (int u = 0; u < g.numU(); u++) {
        if (pairU[u] == NIL) {
            dist[u] = 0;
            q.push(u);
        } else {
            dist[u] = INF;
        }
    }
    
    dist[g.numU()] = INF; // Special NIL vertex (index g.numU())
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        
        if (dist[u] < dist[g.numU()]) {
            // For each neighbor w of u
            for (int w : g.neighborsU(u)) {
                // If w is matched to some vertex v (or NIL)
                int v = pairW[w];
                // v is either NIL or a valid vertex index
                // If v == NIL, we treat it as dist[g.numU()]
                int vIndex = (v == NIL) ? g.numU() : v;
                if (dist[vIndex] == INF) {
                    dist[vIndex] = dist[u] + 1;
                    if (v != NIL) {
                        q.push(v);
                    }
                }
            }
        }
    }
    
    // Return true if we found an augmenting path
    return dist[g.numU()] != INF;
}

// DFS to find augmenting path
bool dfs(const BipartiteGraph& g, int u,
         std::vector<int>& pairU,
         std::vector<int>& pairW,
         std::vector<int>& dist) {
    if (u != NIL) {
        for (int w : g.neighborsU(u)) {
            int v = pairW[w];
            int vIndex = (v == NIL) ? g.numU() : v;
            if (dist[vIndex] == dist[u] + 1) {
                if (dfs(g, v, pairU, pairW, dist)) {
                    pairW[w] = u;
                    pairU[u] = w;
                    return true;
                }
            }
        }
        dist[u] = INF;
        return false;
    }
    return true;
}

// Hopcroft-Karp algorithm to find maximum matching
int hopcroftKarp(const BipartiteGraph& g,
                 std::vector<int>& pairU,
                 std::vector<int>& pairW) {
    int nU = g.numU();
    int nW = g.numW();
    
    pairU.assign(nU + 1, NIL);
    pairW.assign(nW, NIL);
    
    std::vector<int> dist(nU + 1);
    
    int matching = 0;
    
    // Keep finding augmenting paths
    while (bfs(g, pairU, pairW, dist)) {
        for (int u = 0; u < nU; u++) {
            if (pairU[u] == NIL && dfs(g, u, pairU, pairW, dist)) {
                matching++;
            }
        }
    }
    
    return matching;
}

// Build the maximum independent set from the matching
// Using König's theorem and vertex cover construction
std::vector<int> buildMIS(const BipartiteGraph& g,
                          const std::vector<int>& pairU,
                          const std::vector<int>& pairW) {
    int nU = g.numU();
    int nW = g.numW();
    
    // Find minimum vertex cover using König's theorem
    // Then MIS = V \ vertex_cover
    
    // Mark vertices reachable from unmatched U vertices via alternating paths
    std::vector<bool> visitedU(nU, false);
    std::vector<bool> visitedW(nW, false);
    
    std::queue<int> q;
    
    // Start from all unmatched vertices in U
    for (int u = 0; u < nU; u++) {
        if (pairU[u] == NIL) {
            visitedU[u] = true;
            q.push(u);
        }
    }
    
    // BFS via alternating paths
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        
        // Go through ALL edges (U -> W), not just unmatched
        for (int w : g.neighborsU(u)) {
            // Only follow if this is NOT a matched edge from u
            if (pairU[u] != w && !visitedW[w]) {
                visitedW[w] = true;
                
                // Go back via matched edge (W -> U)
                int v = pairW[w];
                if (v != NIL && !visitedU[v]) {
                    visitedU[v] = true;
                    q.push(v);
                }
            }
        }
    }
    
    // Minimum vertex cover:
    // - Unvisited vertices from U
    // - Visited vertices from W
    // Maximum independent set is the complement
    
    std::vector<int> mis;
    
    // Add visited vertices from U to MIS
    for (int u = 0; u < nU; u++) {
        if (visitedU[u]) {
            mis.push_back(u);
        }
    }
    
    // Add unvisited vertices from W to MIS
    for (int w = 0; w < nW; w++) {
        if (!visitedW[w]) {
            mis.push_back(nU + w); // Offset by nU to distinguish from U vertices
        }
    }
    
    return mis;
}

} // anonymous namespace

std::vector<int> maximumIndependentSet(const BipartiteGraph& g) {
    std::vector<int> pairU, pairW;
    
    // Find maximum matching using Hopcroft-Karp
    hopcroftKarp(g, pairU, pairW);
    
    // Build maximum independent set using König's theorem
    return buildMIS(g, pairU, pairW);
}
