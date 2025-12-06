#!/bin/bash
# Run performance benchmark with Python

cd "$(dirname "$0")/.." || exit 1

if [ ! -f "build/min_vertex_cover" ]; then
    echo "Error: Executable not found. Please build the project first:"
    echo "  mkdir -p build && cd build && cmake .. && make"
    exit 1
fi

# Check if Python packages are installed
if ! python3 -c "import matplotlib, numpy" 2>/dev/null; then
    echo "Installing required packages..."
    pip install matplotlib numpy networkx
fi

echo "Running benchmark suite..."
echo

python3 scripts/benchmark.py "$@"
