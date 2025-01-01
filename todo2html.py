import sys
import re
from datetime import datetime

class TodoItem:
    def __init__(self, level=0, description="", due_date=None, tag=None, indent_level=0):
        self.level = level  # Number of + symbols
        self.description = description
        self.due_date = due_date
        self.tag = tag
        self.indent_level = indent_level

def parse_todo_line(line):
    # Remove leading/trailing whitespace
    line = line.strip()
    if not line:
        return None
        
    # Count leading tabs/spaces for indentation
    indent_level = len(line) - len(line.lstrip())
    line = line.lstrip()
    
    # Count + symbols for level
    level = 0
    match = re.match(r'^(\++)\s*', line)
    if match:
        level = len(match.group(1))
        line = line[match.end():]
    
    # Extract tag if present
    tag = None
    if ':' in line:
        line, tag = line.rsplit(':', 1)
        tag = tag.strip()
    
    # Look for date pattern
    due_date = None
    date_match = re.search(r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b', line)
    if date_match:
        due_date = date_match.group(1)
        line = line.replace(due_date, '').strip()
    
    # Clean up description
    description = line.strip()
    
    return TodoItem(level, description, due_date, tag, indent_level)

def generate_html(todos):
    # Get current date for comparison
    current_date = datetime.now()
    
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .todo-item {
            margin: 10px 0;
            padding: 10px;
            border-left: 4px solid #ddd;
            background-color: #fff;
            transition: background-color 0.3s ease;
            cursor: move;
            user-select: none;
        }
        .todo-item:hover {
            border-left-color: #007bff;
        }
        .todo-item.dragging {
            opacity: 0.5;
            background-color: #f8f9fa;
        }
        .todo-item.drag-over {
            border-top: 2px solid #007bff;
        }
        .level-1 { margin-left: 0px; }
        .level-2 { margin-left: 30px; }
        .level-3 { margin-left: 60px; }
        .description {
            font-size: 16px;
            color: #333;
        }
        .due-date {
            font-size: 14px;
            color: #666;
            margin-left: 10px;
        }
        .due-soon {
            color: #f0ad4e;
            font-weight: bold;
        }
        .overdue {
            color: #d9534f;
            font-weight: bold;
        }
        .tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 10px;
        }
        .tag-family {
            background-color: #d4edda;
            color: #155724;
        }
        .tag-work {
            background-color: #cce5ff;
            color: #004085;
        }
        .tag-home {
            background-color: #fff3cd;
            color: #856404;
        }
        .tag-money {
            background-color: #f8d7da;
            color: #721c24;
        }
        .header {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .save-button {
            padding: 8px 16px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .save-button:hover {
            background-color: #218838;
        }
        .save-button:disabled {
            background-color: #6c757d;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span>Todo List</span>
            <button class="save-button" onclick="saveTodoOrder()" disabled>Save Order</button>
        </div>
"""
    
    for todo in todos:
        if todo is None:
            continue
            
        # Determine CSS classes
        classes = [f"todo-item level-{todo.level}"]
        
        # Format due date if present
        date_html = ""
        if todo.due_date:
            try:
                due_date = datetime.strptime(todo.due_date, "%m/%d/%y")
                days_until = (due_date - current_date).days
                date_class = ""
                if days_until < 0:
                    date_class = "overdue"
                elif days_until < 7:
                    date_class = "due-soon"
                date_html = f'<span class="due-date {date_class}">Due: {todo.due_date}</span>'
            except ValueError:
                date_html = f'<span class="due-date">{todo.due_date}</span>'
        
        # Format tag if present
        tag_html = ""
        if todo.tag:
            tag_html = f'<span class="tag tag-{todo.tag.lower()}">{todo.tag}</span>'
        
        # Create a data string with todo information
        todo_data = {
            "description": todo.description,
            "level": todo.level,
            "indent_level": todo.indent_level,
            "due_date": todo.due_date or "",
            "tag": todo.tag or ""
        }
        import json
        todo_data_str = json.dumps(todo_data).replace('"', '&quot;')
        
        html += f"""        <div class="{' '.join(classes)}" draggable="true" data-todo="{todo_data_str}">
            <span class="description">{todo.description}</span>
            {date_html}
            {tag_html}
        </div>
"""
    
    html += """    </div>
    <script>
        let dragSrcEl = null;
        const saveButton = document.querySelector('.save-button');
        let hasChanges = false;

        function handleDragStart(e) {
            this.classList.add('dragging');
            dragSrcEl = this;
            e.dataTransfer.effectAllowed = 'move';
        }

        function handleDragOver(e) {
            if (e.preventDefault) {
                e.preventDefault();
            }
            e.dataTransfer.dropEffect = 'move';
            return false;
        }

        function handleDragEnter(e) {
            this.classList.add('drag-over');
        }

        function handleDragLeave(e) {
            this.classList.remove('drag-over');
        }

        function handleDrop(e) {
            if (e.stopPropagation) {
                e.stopPropagation();
            }

            if (dragSrcEl !== this) {
                const container = document.querySelector('.container');
                const items = Array.from(container.querySelectorAll('.todo-item'));
                const srcIndex = items.indexOf(dragSrcEl);
                const destIndex = items.indexOf(this);

                if (srcIndex < destIndex) {
                    this.parentNode.insertBefore(dragSrcEl, this.nextSibling);
                } else {
                    this.parentNode.insertBefore(dragSrcEl, this);
                }

                hasChanges = true;
                saveButton.disabled = false;
            }

            return false;
        }

        function handleDragEnd(e) {
            this.classList.remove('dragging');
            document.querySelectorAll('.todo-item').forEach(item => {
                item.classList.remove('drag-over');
            });
        }

        function saveTodoOrder() {
            const items = document.querySelectorAll('.todo-item');
            const todos = Array.from(items).map(item => {
                return JSON.parse(item.getAttribute('data-todo'));
            });

            // Convert todos to text format
            const todoText = todos.map(todo => {
                const indent = ' '.repeat(todo.indent_level);
                const level = '+'.repeat(todo.level);
                let line = `${indent}${level} ${todo.description}`;
                if (todo.due_date) {
                    line += ` ${todo.due_date}`;
                }
                if (todo.tag) {
                    line += ` :${todo.tag}`;
                }
                return line;
            }).join('\\n');

            // Create a temporary textarea to copy the content
            const textarea = document.createElement('textarea');
            textarea.value = todoText;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);

            // Update button state
            saveButton.disabled = true;
            hasChanges = false;
            saveButton.textContent = 'Copied to Clipboard!';
            setTimeout(() => {
                saveButton.textContent = 'Save Order';
            }, 2000);

            // Show instructions
            alert('The new todo list has been copied to your clipboard.\\n\\nTo save the changes:\\n1. Open todos.txt in your text editor\\n2. Replace the entire content with the copied text (Ctrl+A, Ctrl+V)\\n3. Save the file\\n4. Run generate_todo.sh again to update the HTML');
        }

        document.querySelectorAll('.todo-item').forEach(item => {
            item.addEventListener('dragstart', handleDragStart);
            item.addEventListener('dragover', handleDragOver);
            item.addEventListener('dragenter', handleDragEnter);
            item.addEventListener('dragleave', handleDragLeave);
            item.addEventListener('dragend', handleDragEnd);
            item.addEventListener('drop', handleDrop);
        });
    </script>
</body>
</html>"""
    
    return html

def main():
    todos = []
    for line in sys.stdin:
        todo = parse_todo_line(line)
        if todo:
            todos.append(todo)
    
    print(generate_html(todos))

if __name__ == "__main__":
    main()