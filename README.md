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
chmod +x html2todo.sh
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

Basic usage (looks for todos.html in current directory):
```bash
./html2todo.sh
```

Specify input and output files:
```bash
./html2todo.sh -i my-todos.html -o output.txt
```

Show help message:
```bash
./html2todo.sh --help
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
- `generate_todo.sh`: Script to convert text to HTML
- `html2todo.sh`: Script to convert HTML back to text
- `todo2html.py`: Core HTML generation logic
- `html2todo.py`: Core text generation logic
- `todos.txt`: Sample todo list