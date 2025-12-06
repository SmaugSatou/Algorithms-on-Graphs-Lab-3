#!/usr/bin/env python3
"""Generate large test cases for stress testing and benchmarking."""

import random
import os
from typing import Tuple, List


def generate_graph(nU: int, nW: int, num_edges: int, filename: str) -> None:
    """Generate a random bipartite graph test file.

    Args:
        nU: Number of vertices in set U.
        nW: Number of vertices in set W.
        num_edges: Number of edges to generate.
        filename: Output file path.
    """
    edges = set()

    # Ensure we don't generate more edges than possible
    max_edges = nU * nW
    num_edges = min(num_edges, max_edges)

    # Generate random edges
    while len(edges) < num_edges:
        u = random.randint(0, nU - 1)
        w = random.randint(0, nW - 1)
        edges.add((u, w))

    # Write to file
    with open(filename, 'w') as f:
        f.write(f"{nU}\n")
        f.write(f"{nW}\n")
        f.write(f"{len(edges)}\n")
        for u, w in sorted(edges):
            f.write(f"{u} {w}\n")

    print(f"Generated: {filename} (U={nU}, W={nW}, edges={len(edges)})")


def main() -> None:
    """Generate all test configurations."""
    os.makedirs('tests', exist_ok=True)

    print("Generating large test cases...")
    print("="*70)

    # Small to very large tests for comprehensive benchmarking
    test_configs = [
        # (nU, nW, edges, filename)
        (10, 10, 20, 'tests/test_small_sparse.txt'),
        (10, 10, 50, 'tests/test_small_dense.txt'),
        (50, 50, 100, 'tests/test_medium_sparse.txt'),
        (50, 50, 500, 'tests/test_medium_medium.txt'),
        (50, 50, 1500, 'tests/test_medium_dense.txt'),
        (100, 100, 200, 'tests/test_large_sparse.txt'),
        (100, 100, 1000, 'tests/test_large_medium.txt'),
        (100, 100, 5000, 'tests/test_large_dense.txt'),
        (200, 150, 500, 'tests/test_xlarge_sparse.txt'),
        (200, 150, 3000, 'tests/test_xlarge_medium.txt'),
        (300, 300, 1000, 'tests/test_xxlarge_sparse.txt'),
        (300, 300, 10000, 'tests/test_xxlarge_medium.txt'),
        # Additional very large tests
        (500, 500, 2500, 'tests/test_huge_sparse.txt'),
        (500, 500, 15000, 'tests/test_huge_medium.txt'),
        (500, 500, 50000, 'tests/test_huge_dense.txt'),
        (1000, 1000, 5000, 'tests/test_massive_sparse.txt'),
        (1000, 1000, 50000, 'tests/test_massive_medium.txt'),
        (1000, 1000, 200000, 'tests/test_massive_dense.txt'),
        (2000, 2000, 10000, 'tests/test_enormous_sparse.txt'),
        (2000, 2000, 100000, 'tests/test_enormous_medium.txt'),
        (5000, 5000, 25000, 'tests/test_gigantic_sparse.txt'),
        (5000, 5000, 250000, 'tests/test_gigantic_medium.txt'),
    ]

    for nU, nW, edges, filename in test_configs:
        generate_graph(nU, nW, edges, filename)

    print("="*70)
    print(f"Generated {len(test_configs)} test files")
    print("\nRun tests with:")
    print("  ./scripts/run_all_tests.sh")
    print("  ./scripts/verify_with_networkx.sh")


if __name__ == "__main__":
    main()
