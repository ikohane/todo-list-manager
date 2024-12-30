#!/bin/bash

# Default input and output files
input_file="todos.html"
output_file="exported_todos.txt"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -i|--input) input_file="$2"; shift ;;
        -o|--output) output_file="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Check if input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' not found!"
    exit 1
fi

# Install BeautifulSoup4 if not already installed
if ! python3 -c "import bs4" 2>/dev/null; then
    echo "Installing required Python package: beautifulsoup4"
    pip3 install beautifulsoup4
fi

# Convert HTML to todo list
cat "$input_file" | python3 html2todo.py > "$output_file"

echo "HTML has been converted to todo list: $output_file"