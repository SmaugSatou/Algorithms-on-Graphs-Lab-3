#!/usr/bin/env python3
"""Performance benchmark for Maximum Independent Set algorithm.

Compares C++ implementation with NetworkX and generates visualization graphs.
"""

import subprocess
import time
import os
import sys
import glob
from typing import Dict, List, Tuple, Optional, Any
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

try:
    import networkx as nx
    from networkx.algorithms import bipartite
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    print("Warning: NetworkX not available. Install with: pip install networkx")


def read_graph_from_file(filename: str) -> Dict[str, Any]:
    """Read graph data from test file.
    
    Args:
        filename: Path to the test file.
        
    Returns:
        Dictionary containing nU, nW, edges, and filename.
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
    
    return {'nU': nU, 'nW': nW, 'edges': edges, 'filename': filename}


def run_cpp_implementation(
    graph_data: Dict[str, Any], 
    executable: str = './build/min_vertex_cover', 
    num_runs: int = 10
) -> Optional[Dict[str, Any]]:
    """Benchmark C++ implementation.
    
    Args:
        graph_data: Dictionary containing graph information.
        executable: Path to the C++ executable.
        num_runs: Number of benchmark runs.
        
    Returns:
        Dictionary with timing statistics and MIS size, or None on error.
    """
    if not os.path.exists(executable):
        print(f"Error: {executable} not found")
        return None
    
    filename = graph_data['filename']
    times = []
    
    for _ in range(num_runs):
        start = time.perf_counter()
        result = subprocess.run(
            [executable, filename],
            capture_output=True,
            text=True,
            timeout=30
        )
        times.append(time.perf_counter() - start)
        
        if result.returncode != 0:
            return None
    
    mis_size = None
    for line in result.stdout.split('\n'):
        if line.startswith('Size:'):
            mis_size = int(line.split(':')[1].strip())
            break
    
    return {
        'times': times,
        'avg_time': np.mean(times) * 1000,
        'std_time': np.std(times) * 1000,
        'mis_size': mis_size
    }


def run_networkx_implementation(
    graph_data: Dict[str, Any], 
    num_runs: int = 10
) -> Optional[Dict[str, Any]]:
    """Benchmark NetworkX implementation.
    
    Args:
        graph_data: Dictionary containing graph information.
        num_runs: Number of benchmark runs.
        
    Returns:
        Dictionary with timing statistics and MIS size, or None if unavailable.
    """
    if not NETWORKX_AVAILABLE:
        return None
    
    G = nx.Graph()
    nU = graph_data['nU']
    nW = graph_data['nW']
    
    U_nodes = [f'U{i}' for i in range(nU)]
    W_nodes = [f'W{i}' for i in range(nW)]
    
    G.add_nodes_from(U_nodes, bipartite=0)
    G.add_nodes_from(W_nodes, bipartite=1)
    
    for u, w in graph_data['edges']:
        G.add_edge(f'U{u}', f'W{w}')
    
    times = []
    for _ in range(num_runs):
        start = time.perf_counter()
        matching = bipartite.maximum_matching(G, top_nodes=set(U_nodes))
        matching_size = len(matching) // 2
        mis_size = nU + nW - matching_size
        times.append(time.perf_counter() - start)
    
    return {
        'times': times,
        'avg_time': np.mean(times) * 1000,
        'std_time': np.std(times) * 1000,
        'mis_size': mis_size
    }


def benchmark_test_files(
    test_files: List[str], 
    num_runs: int = 10
) -> List[Dict[str, Any]]:
    """Run benchmarks on multiple test files.
    
    Args:
        test_files: List of test file paths.
        num_runs: Number of benchmark runs per file.
        
    Returns:
        List of benchmark result dictionaries.
    """
    results = []
    
    for test_file in test_files:
        print(f"Benchmarking {os.path.basename(test_file)}...", end=' ')
        
        graph_data = read_graph_from_file(test_file)
        vertices = graph_data['nU'] + graph_data['nW']
        edges = len(graph_data['edges'])
        
        # C++ benchmark
        cpp_result = run_cpp_implementation(graph_data, num_runs=num_runs)
        
        # NetworkX benchmark
        nx_result = run_networkx_implementation(graph_data, num_runs=num_runs)
        
        if cpp_result:
            result = {
                'filename': os.path.basename(test_file),
                'vertices': vertices,
                'edges': edges,
                'nU': graph_data['nU'],
                'nW': graph_data['nW'],
                'mis_size': cpp_result['mis_size'],
                'cpp_time': cpp_result['avg_time'],
                'cpp_std': cpp_result['std_time'],
                'nx_time': nx_result['avg_time'] if nx_result else None,
                'nx_std': nx_result['std_time'] if nx_result else None,
                'speedup': nx_result['avg_time'] / cpp_result['avg_time'] if nx_result else None
            }
            results.append(result)
            print(f"{cpp_result['avg_time']:.2f}ms")
        else:
            print("Failed")
    
    return results


def plot_performance_comparison(results: List[Dict[str, Any]], output_dir: str) -> None:
    """Generate performance comparison plot.
    
    Args:
        results: List of benchmark result dictionaries.
        output_dir: Directory to save the plot.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    vertices = [r['vertices'] for r in results]
    cpp_times = [r['cpp_time'] for r in results]
    nx_times = [r['nx_time'] for r in results if r['nx_time'] is not None]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(results))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, cpp_times, width, label='C++ Implementation', color='steelblue')
    if nx_times:
        bars2 = ax.bar(x + width/2, nx_times, width, label='NetworkX (Python)', color='coral')
    
    ax.set_xlabel('Test Cases', fontweight='bold')
    ax.set_ylabel('Average Time (ms)', fontweight='bold')
    ax.set_title('Performance Comparison: C++ vs NetworkX', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{r['vertices']}v\n{r['edges']}e" for r in results], rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/benchmark.png', dpi=150)
    print(f"Saved: {output_dir}/benchmark.png")
    plt.close()


def save_results_table(results: List[Dict[str, Any]], output_dir: str) -> None:
    """Save results as text table.
    
    Args:
        results: List of benchmark result dictionaries.
        output_dir: Directory to save the results file.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/results.txt', 'w') as f:
        f.write(f"{'Test':<30} {'Vertices':<10} {'Edges':<10} {'MIS':<8} {'C++ (ms)':<12} {'NetworkX (ms)':<15}\n")
        f.write("-"*85 + "\n")
        
        for r in results:
            nx_time_str = f"{r['nx_time']:.4f}" if r['nx_time'] else "N/A"
            f.write(f"{r['filename']:<30} {r['vertices']:<10} {r['edges']:<10} {r['mis_size']:<8} "
                   f"{r['cpp_time']:<12.4f} {nx_time_str:<15}\n")
        
        f.write("\n")
        f.write(f"Average C++ time: {np.mean([r['cpp_time'] for r in results]):.4f} ms\n")
        if any(r['nx_time'] for r in results):
            nx_times = [r['nx_time'] for r in results if r['nx_time']]
            f.write(f"Average NetworkX time: {np.mean(nx_times):.4f} ms\n")
    
    print(f"Saved: {output_dir}/results.txt")


def main() -> None:
    """Main entry point for benchmark script."""
    print("="*70)
    print("Maximum Independent Set - Performance Benchmark")
    print("="*70)
    print()
    
    # Get test files
    if len(sys.argv) > 1:
        test_files = sys.argv[1:]
    else:
        test_files = sorted(glob.glob('tests/test*.txt'))
    
    if not test_files:
        print("No test files found")
        return
    
    print(f"Found {len(test_files)} test files")
    print()
    
    # Run benchmarks
    results = benchmark_test_files(test_files, num_runs=20)
    
    if not results:
        print("No results to display")
        return
    
    # Create output directory
    output_dir = 'results'
    
    # Generate visualization and save results
    print()
    plot_performance_comparison(results, output_dir)
    save_results_table(results, output_dir)
    
    print()
    print(f"Tests completed: {len(results)}")
    print(f"Average C++ time: {np.mean([r['cpp_time'] for r in results]):.4f} ms")
    if any(r['nx_time'] for r in results):
        nx_times = [r['nx_time'] for r in results if r['nx_time']]
        print(f"Average NetworkX time: {np.mean(nx_times):.4f} ms")
    print(f"Results saved in '{output_dir}/' directory")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease install required packages:")
        print("  pip install matplotlib numpy networkx")
