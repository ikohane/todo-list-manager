#!/bin/bash

# Default input and output files
input_file="todos.html"
output_file="todos.txt"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -i|--input) input_file="$2"; shift ;;
        -o|--output) output_file="$2"; shift ;;
        -h|--help)
            echo "Usage: $0 [-i input.html] [-o output.txt]"
            echo "Convert HTML todo list back to text format"
            echo ""
            echo "Options:"
            echo "  -i, --input     Input HTML file (default: todos.html)"
            echo "  -o, --output    Output text file (default: todos.txt)"
            echo "  -h, --help      Show this help message"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Check if input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' not found!"
    exit 1
fi

# Convert HTML to text using the Python script
python3 html2todo.py "$input_file" "$output_file"

echo "HTML has been converted to text: $output_file"