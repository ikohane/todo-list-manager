# Todo List Manager

A tool for converting structured todo lists between text and HTML formats, with support for heading levels, due dates, and tags.

## Getting Started

1. Clone the repository:
```bash
cd /workspace
git clone https://github.com/ikohane/todo-list-manager.git
cd todo-list-manager
```

2. Make sure the scripts are executable:
```bash
chmod +x generate_todo.sh
chmod +x html2todo.py
```

## Todo List Format

The text format supports:
- Heading levels using +, ++, or +++
- Due dates in MM/DD/YY format
- Tags: home, family, work, money

Example:
```
+ Project Name
++ Task with due date 12/31/24
++ Task with tag : work
++ Task with both 12/31/24 : family
```

## Usage

### Convert Text to HTML

Basic usage (looks for todos.txt in current directory):
```bash
./generate_todo.sh
```

Specify input and output files:
```bash
./generate_todo.sh -i my-todos.txt -o output.html
```

### Convert HTML back to Text

Convert an HTML file back to text format:
```bash
python3 html2todo.py todos.html new_todos.txt
```

## Features

### HTML Output
- Clean, modern styling
- Responsive layout
- Color-coded tags
- Due date highlighting
- Visual hierarchy for heading levels

### Text Format
- Flexible syntax
- Human-readable
- Easy to edit
- Preserves structure when converting back from HTML

## File Structure
- `generate_todo.sh`: Main conversion script
- `todo2html.py`: Core HTML generation logic
- `html2todo.py`: HTML to text conversion
- `todos.txt`: Sample todo list