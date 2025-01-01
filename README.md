# Todo List Manager

A simple yet powerful tool to convert text-based todo lists into beautifully formatted HTML pages. This tool allows you to maintain your todos in a simple text format and generate a visually appealing, interactive HTML view.

## Features

- **Priority Levels**: Use `+` symbols to indicate priority/hierarchy levels
- **Due Dates**: Add dates in format `MM/DD/YY` or `MM/DD/YYYY`
- **Tags**: Add categories using `:tag` format (e.g., `:work`, `:family`, `:home`, `:money`)
- **Indentation**: Support for nested tasks using spaces or tabs
- **Visual Indicators**: 
  - Overdue tasks are highlighted in red
  - Tasks due within 7 days are highlighted in yellow
  - Color-coded tags for different categories
- **Interactive UI**: Hover effects and clean, modern design

## File Format

The todo list should be maintained in a text file with the following format:

```
+ Main Task
++ Subtask with due date MM/DD/YY
++ Another subtask :tag
        ++ Indented task with tag :family
```

- Use `+` or multiple `++` to indicate hierarchy levels
- Add due dates in MM/DD/YY format anywhere in the task description
- Add tags at the end of the line using `:tagname`
- Use spaces or tabs for indentation

## Usage

1. Create your todo list in a text file (default: `todos.txt`)
2. Run the conversion script:

```bash
./generate_todo.sh
```

Or specify custom input/output files:

```bash
./generate_todo.sh -i input.txt -o output.html
```

### Command Line Options

- `-i, --input`: Specify input file (default: todos.txt)
- `-o, --output`: Specify output file (default: todos.html)

## Output

The script generates a responsive HTML file with:
- Clean, modern design
- Visual hierarchy for tasks
- Color-coded due dates and tags
- Hover effects for better interaction
- Mobile-friendly layout

## Requirements

- Python 3
- Bash shell
- Modern web browser for viewing the output

## Example

Input text:
```
+ Work Project
++ Complete documentation 12/25/23 :work
++ Review code changes
        ++ Update unit tests 12/30/23
+ Personal
++ Buy groceries :home
++ Pay bills 12/28/23 :money
```

This will generate an HTML file with a beautifully formatted todo list, including due date highlighting and tag categorization.