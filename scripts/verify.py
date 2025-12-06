#!/usr/bin/env python3
"""Verify C++ implementation correctness against NetworkX."""

import sys
import subprocess
from typing import Dict, List, Tuple, Optional
import networkx as nx


def read_graph_from_file(filename: str) -> Dict[str, any]:
    """Read graph data from test file.
    
    Args:
        filename: Path to the test file.
        
    Returns:
        Dictionary containing nU, nW, and edges list.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    nU = int(lines[0].strip())
    nW = int(lines[1].strip())
    m = int(lines[2].strip())
    
    edges = []
    for i in range(3, 3 + m):
        u, w = map(int, lines[i].strip().split())
        edges.append((u, w))
    
    return {'nU': nU, 'nW': nW, 'edges': edges}


def networkx_mis_size(graph_data: Dict[str, any]) -> int:
    """Calculate exact MIS size using NetworkX maximum matching and König's theorem.
    
    Args:
        graph_data: Dictionary with nU, nW, and edges.
        
    Returns:
        Size of the maximum independent set (exact).
    """
    G = nx.Graph()
    nU = graph_data['nU']
    nW = graph_data['nW']
    
    U_nodes = [f'U{i}' for i in range(nU)]
    W_nodes = [f'W{i}' for i in range(nW)]
    
    G.add_nodes_from(U_nodes, bipartite=0)
    G.add_nodes_from(W_nodes, bipartite=1)
    
    for u, w in graph_data['edges']:
        G.add_edge(f'U{u}', f'W{w}')
    
    from networkx.algorithms import bipartite
    matching = bipartite.maximum_matching(G, top_nodes=set(U_nodes))
    max_matching_size = len(matching) // 2
    
    # König's theorem: MIS size = Total vertices - Maximum matching size
    mis_size = nU + nW - max_matching_size
    
    return mis_size


def cpp_mis_size(filename: str, executable: str = './build/min_vertex_cover') -> Optional[int]:
    """Get MIS size from C++ implementation.
    
    Args:
        filename: Path to the test file.
        executable: Path to the C++ executable.
        
    Returns:
        MIS size or None if execution failed.
    """
    result = subprocess.run(
        [executable, filename],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    for line in result.stdout.split('\n'):
        if line.startswith('Size:'):
            return int(line.split(':')[1].strip())
    
    return None


def verify_file(filename: str) -> bool:
    """Verify a single test file.
    
    Args:
        filename: Path to the test file.
        
    Returns:
        True if verification passed, False otherwise.
    """
    print(f"Verifying {filename}...", end=' ', flush=True)
    
    graph_data = read_graph_from_file(filename)
    
    nx_size = networkx_mis_size(graph_data)
    cpp_size = cpp_mis_size(filename)
    
    if cpp_size is None:
        print("FAIL (C++ execution error)", flush=True)
        return False
    
    # Both algorithms should give exact same result (König's theorem)
    if cpp_size == nx_size:
        print(f"PASS (MIS size: {cpp_size})", flush=True)
        return True
    else:
        print(f"FAIL (C++ found {cpp_size}, NetworkX found {nx_size})", flush=True)
        return False


def main() -> int:
    """Main entry point for verification script.
    
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if len(sys.argv) < 2:
        print("Usage: python verify.py <test_file1> [test_file2 ...]")
        print("Example: python scripts/verify.py tests/test*.txt")
        return
    
    test_files = sys.argv[1:]
    passed = 0
    failed = 0
    
    test_files = sys.argv[1:]
    passed = 0
    failed = 0
    
    print("="*70)
    print("Verification Against NetworkX (Exact Algorithm)")
    print("Both implementations use König's theorem for exact MIS")
    print("="*70)
    print()
    
    for test_file in test_files:
        if verify_file(test_file):
            passed += 1
        else:
            failed += 1
    
    print()
    print("="*70)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*70)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ImportError:
        print("Error: NetworkX not installed")
        print("Install with: pip install networkx")
        sys.exit(1)
