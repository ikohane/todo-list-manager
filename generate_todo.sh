#!/bin/bash

# Default input and output files
input_file="todos.txt"
output_file="todos.html"

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

# Convert todo list to HTML
cat "$input_file" | python3 todo2html.py > "$output_file"

echo "Todo list has been converted to HTML: $output_file"

# If we're in the OpenHands environment, try to display the file
if [ -f "$output_file" ]; then
    echo "To view the todo list in the OpenHands browser, use:"
    echo 'browser.goto("file://'"$(realpath "$output_file")"'")'
fi