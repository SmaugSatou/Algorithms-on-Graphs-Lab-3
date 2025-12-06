#!/bin/bash
# Run all tests with the C++ implementation

echo "======================================================================"
echo "Running All Test Cases"
echo "======================================================================"
echo

cd "$(dirname "$0")/.." || exit 1

if [ ! -f "build/min_vertex_cover" ]; then
    echo "Error: Executable not found. Please build the project first:"
    echo "  mkdir -p build && cd build && cmake .. && make"
    exit 1
fi

# Create results directory
mkdir -p results

# Output file
OUTPUT_FILE="results/test_results.txt"

# Clear previous results
> "$OUTPUT_FILE"

echo "Running tests and saving results to $OUTPUT_FILE..."
echo

# Header
{
    echo "======================================================================"
    echo "Maximum Independent Set - Test Results"
    echo "Date: $(date)"
    echo "======================================================================"
    echo
} >> "$OUTPUT_FILE"

# Run tests and save to file
for test_file in tests/test*.txt; do
    if [ -f "$test_file" ]; then
        {
            echo "----------------------------------------------------------------------"
            echo "Test: $(basename "$test_file")"
            echo "----------------------------------------------------------------------"
            ./build/min_vertex_cover "$test_file"
            echo
        } >> "$OUTPUT_FILE"
        
        # Show progress in terminal
        echo "  Completed: $(basename "$test_file")"
    fi
done

{
    echo "======================================================================"
    echo "All tests completed"
    echo "======================================================================"
} >> "$OUTPUT_FILE"

echo
echo "======================================================================"
echo "Verifying Results with NetworkX"
echo "======================================================================"
echo

VERIFY_FILE="results/verification.txt"
> "$VERIFY_FILE"

if [ -f "scripts/verify.py" ]; then
    python3 -u scripts/verify.py tests/test*.txt 2>&1 | tee "$VERIFY_FILE"
else
    echo "Warning: verify.py not found"
fi

