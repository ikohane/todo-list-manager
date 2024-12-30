#!/bin/bash

# Default input and output files
input_file="todos.html"
original_todo="todos.txt"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -i|--input) input_file="$2"; shift ;;
        -t|--todo) original_todo="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Check if input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' not found!"
    exit 1
fi

# Check if original todo file exists
if [ ! -f "$original_todo" ]; then
    echo "Error: Original todo file '$original_todo' not found!"
    exit 1
fi

# Create backup with timestamp
timestamp=$(date "+%Y%m%d_%H%M%S")
backup_file="${original_todo%.*}_OLD_${timestamp}.txt"
cp "$original_todo" "$backup_file"
echo "Created backup: $backup_file"

# Install BeautifulSoup4 if not already installed
if ! python3 -c "import bs4" 2>/dev/null; then
    echo "Installing required Python package: beautifulsoup4"
    pip3 install beautifulsoup4
fi

# Convert HTML to todo list
echo "Converting HTML to todo list..."
if cat "$input_file" | python3 html2todo.py > "$original_todo"; then
    echo "Successfully converted HTML and updated: $original_todo"
    echo "Previous version backed up as: $backup_file"
else
    echo "Error during conversion! Restoring from backup..."
    cp "$backup_file" "$original_todo"
    exit 1
fi