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
        self.is_header = False
        self.is_done = False

def parse_todo_line(line, is_done=False):
    # Remove leading/trailing whitespace
    line = line.strip()
    if not line:
        return None
    if line == "DONE":
        return "DONE_MARKER"
        
    # Count leading tabs/spaces for indentation
    indent_level = len(line) - len(line.lstrip())
    line = line.lstrip()
    
    # Count + symbols for level
    level = 0
    match = re.match(r'^(\++)\s*', line)
    if match:
        level = len(match.group(1))
        line = line[match.end():]
    else:
        # If no + symbols and no other markers, treat as a header
        if not re.search(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', line) and ':' not in line:
            level = 1
            todo = TodoItem(level, line, None, None, indent_level)
            todo.is_header = True
            return todo
    
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
    
    todo = TodoItem(level, description, due_date, tag, indent_level)
    todo.is_done = is_done
    todo.is_header = False
    return todo

def generate_todo_html(todos, is_done=False):
    html = ""
    current_section = None
    
    for todo in todos:
        if todo is None:
            continue
            
        # Determine CSS classes
        classes = [f"todo-item level-{todo.level}"]
        if is_done:
            classes.append("done")
        if todo.is_header:
            classes.append("header")
            # Close previous section if exists
            if current_section is not None:
                html += "        </div>\n"
            # Start new section
            html += '        <div class="todo-section">\n'
            current_section = todo.description
        
        # Format due date if present
        date_html = ""
        if todo.due_date:
            try:
                due_date = datetime.strptime(todo.due_date, "%m/%d/%y")
                current_time = datetime.now()
                days_until = (due_date - current_time).days
                date_class = "date-future" if due_date > current_time else "date-past"
                date_html = f'<span class="due-date {date_class}">Due: {todo.due_date}</span>'
            except ValueError:
                date_html = f'<span class="due-date">{todo.due_date}</span>'
        
        # Format tag if present
        tag_html = ""
        if todo.tag:
            tag_html = f'<span class="tag tag-{todo.tag.lower()}">{todo.tag}</span>'
        
        # Add drag handle
        drag_html = '<span class="drag-handle">⋮⋮</span>'
        
        html += f"""            <div class="{' '.join(classes)}">
                {drag_html}
                <span class="description">{todo.description}</span>
                {date_html}
                {tag_html}
            </div>
"""
    
    # Close last section if exists
    if current_section is not None:
        html += "        </div>\n"
    return html

def main():
    active_todos = []
    done_todos = []
    is_done_section = False
    
    for line in sys.stdin:
        todo = parse_todo_line(line, is_done_section)
        if todo == "DONE_MARKER":
            is_done_section = True
        elif todo:
            if is_done_section:
                done_todos.append(todo)
            else:
                active_todos.append(todo)
    
    # Start HTML generation
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            max-width: 600px;
            margin: 20px auto;
            padding: 10px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .todo-item {
            margin: 5px 0;
            padding: 5px;
            border-left: 4px solid #ddd;
            background-color: #fff;
            transition: all 0.3s ease;
        }
        .todo-item:hover {
            transform: translateX(5px);
            border-left-color: #007bff;
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
            flex-wrap: wrap;
        }
        .timestamp {
            font-size: 14px;
            color: #666;
            flex-basis: 100%;
            margin-top: 10px;
            text-align: right;
        }
        .date-past {
            color: #dc3545 !important;
        }
        .date-future {
            color: #0056b3 !important;
        }
        .export-button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s;
        }
        .export-button:hover {
            background-color: #0056b3;
        }
        .done-separator {
            margin: 30px 0;
            border-top: 2px dashed #ccc;
            position: relative;
        }
        .done-label {
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background-color: white;
            padding: 0 15px;
            color: #888;
            font-size: 14px;
        }
        .todo-item.done {
            opacity: 0.6;
            border-left-color: #ccc;
        }
        .todo-item.done:hover {
            border-left-color: #888;
        }
        .todo-item.header {
            border-left: none !important;
            margin-top: 15px;
            margin-bottom: 10px;
            padding: 0;
            background: none;
        }
        .todo-item.header .description {
            font-size: 22px;
            font-weight: 500;
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 8px;
            display: block;
            width: 100%;
        }
        .todo-item.header:hover {
            transform: none;
        }
        .drag-handle {
            cursor: grab;
            color: #ccc;
            padding: 0 8px;
            visibility: hidden;
            user-select: none;
        }
        .todo-item:hover .drag-handle {
            visibility: visible;
        }
        .todo-item.dragging {
            opacity: 0.5;
            background-color: #f8f9fa;
        }
        .todo-section {
            margin-bottom: 20px;
        }
        .drop-target {
            border: 2px dashed #007bff;
            margin: 10px 0;
            height: 4px;
            display: none;
        }
        .todo-item.header:first-child {
            margin-top: 0;
        }
    </style>
    <script>
        function initDragAndDrop() {
            const items = document.querySelectorAll('.todo-item');
            const sections = document.querySelectorAll('.todo-section');
            
            items.forEach(item => {
                const handle = item.querySelector('.drag-handle');
                if (!handle) return;
                
                handle.addEventListener('mousedown', e => {
                    e.preventDefault();
                    item.classList.add('dragging');
                    
                    const startY = e.clientY;
                    const startTop = item.offsetTop;
                    const parent = item.parentElement;
                    const isHeader = item.classList.contains('header');
                    
                    // Create drop targets
                    const dropTargets = [];
                    if (isHeader) {
                        sections.forEach(section => {
                            const target = document.createElement('div');
                            target.className = 'drop-target';
                            section.parentElement.insertBefore(target, section);
                            dropTargets.push(target);
                        });
                    } else {
                        const currentSection = item.closest('.todo-section');
                        const sectionItems = currentSection.querySelectorAll('.todo-item:not(.header)');
                        sectionItems.forEach(sectionItem => {
                            const target = document.createElement('div');
                            target.className = 'drop-target';
                            sectionItem.parentElement.insertBefore(target, sectionItem);
                            dropTargets.push(target);
                        });
                    }
                    
                    const moveHandler = e => {
                        const deltaY = e.clientY - startY;
                        item.style.transform = `translateY(${deltaY}px)`;
                        
                        // Show nearest drop target
                        const itemRect = item.getBoundingClientRect();
                        const itemCenter = itemRect.top + itemRect.height / 2;
                        
                        dropTargets.forEach(target => {
                            const targetRect = target.getBoundingClientRect();
                            const distance = Math.abs(targetRect.top - itemCenter);
                            if (distance < 30) {
                                target.style.display = 'block';
                            } else {
                                target.style.display = 'none';
                            }
                        });
                    };
                    
                    const upHandler = e => {
                        document.removeEventListener('mousemove', moveHandler);
                        document.removeEventListener('mouseup', upHandler);
                        item.classList.remove('dragging');
                        item.style.transform = '';
                        
                        // Find nearest drop target
                        const itemRect = item.getBoundingClientRect();
                        const itemCenter = itemRect.top + itemRect.height / 2;
                        let nearestTarget = null;
                        let minDistance = Infinity;
                        
                        dropTargets.forEach(target => {
                            const targetRect = target.getBoundingClientRect();
                            const distance = Math.abs(targetRect.top - itemCenter);
                            if (distance < minDistance) {
                                minDistance = distance;
                                nearestTarget = target;
                            }
                        });
                        
                        // Move item to new position
                        if (nearestTarget && minDistance < 30) {
                            if (isHeader) {
                                const targetSection = nearestTarget.nextElementSibling;
                                if (targetSection) {
                                    parent.insertBefore(item.closest('.todo-section'), targetSection);
                                } else {
                                    parent.appendChild(item.closest('.todo-section'));
                                }
                            } else {
                                const targetItem = nearestTarget.nextElementSibling;
                                if (targetItem) {
                                    parent.insertBefore(item, targetItem);
                                } else {
                                    parent.appendChild(item);
                                }
                            }
                        }
                        
                        // Remove drop targets
                        dropTargets.forEach(target => target.remove());
                    };
                    
                    document.addEventListener('mousemove', moveHandler);
                    document.addEventListener('mouseup', upHandler);
                });
            });
        }
        
        function exportToText() {
            const htmlContent = document.documentElement.outerHTML;
            const blob = new Blob([htmlContent], { type: 'text/html' });
            const formData = new FormData();
            formData.append('html_file', blob, 'todos.html');
            
            fetch('http://localhost:8000/export', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(text => {
                const textBlob = new Blob([text], { type: 'text/plain' });
                const downloadUrl = URL.createObjectURL(textBlob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = 'exported_todos.txt';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(downloadUrl);
            })
            .catch(error => {
                console.error('Export failed:', error);
                const command = './export_todo.sh -i todos.html';
                alert('Server not available. Running local export script: ' + command);
            });
        }
    </script>
</head>
<body onload="initDragAndDrop()">
    <div class="container">
        <div class="header">
            <span>Todo List</span>
            <button class="export-button" onclick="exportToText()">Export to Text</button>
            <div class="timestamp">Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</div>
        </div>"""
    
    # Add active todos
    html += generate_todo_html(active_todos)
    
    # Add separator if there are done todos
    if done_todos:
        html += """        <div class="done-separator">
            <span class="done-label">Completed Tasks</span>
        </div>"""
        html += generate_todo_html(done_todos, is_done=True)
    
    # Close HTML
    html += """    </div>
</body>
</html>"""
    
    print(html)

if __name__ == "__main__":
    main()