#!/usr/bin/env python3
from bs4 import BeautifulSoup
import sys

def html_to_todo(html_file):
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    todo_items = soup.find_all(class_='todo-item')
    todo_text = ''
    
    for item in todo_items:
        # Get level from class
        level = 1
        if 'level-2' in item['class']:
            level = 2
        elif 'level-3' in item['class']:
            level = 3
        
        # Add the appropriate number of + symbols
        prefix = '+' * level
        
        # Get description
        description = item.find(class_='description').text.strip()
        
        # Get due date if it exists
        due_date = item.find(class_='due-date')
        due_date = due_date.text.replace('Due: ', '') if due_date else ''
        
        # Get tag if it exists
        tag = item.find(class_='tag')
        tag = tag.text if tag else ''
        
        # Build the line
        line = f"{prefix} {description}"
        if due_date:
            line += f" {due_date}"
        if tag:
            line += f" : {tag}"
        
        todo_text += line + '\n'
    
    return todo_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 html2todo.py input.html [output.txt]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'converted_todos.txt'
    
    todo_text = html_to_todo(html_file)
    
    with open(output_file, 'w') as f:
        f.write(todo_text)
    
    print(f"Todo list has been converted and saved to: {output_file}")