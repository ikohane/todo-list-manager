#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup
import re

def extract_level(classes):
    if isinstance(classes, list):
        classes = ' '.join(classes)
    level_match = re.search(r'level-(\d+)', str(classes))
    return int(level_match.group(1)) if level_match else 0

def extract_due_date(todo_item):
    due_date_span = todo_item.find('span', class_='due-date')
    if due_date_span:
        date_text = due_date_span.text
        match = re.search(r'Due: (.+)', date_text)
        return match.group(1) if match else None
    return None

def extract_tag(todo_item):
    tag_span = todo_item.find('span', class_='tag')
    if tag_span:
        return tag_span.text
    return None

def html_to_todo(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    todos = []
    
    for todo_item in soup.find_all('div', class_='todo-item'):
        # Get level
        level = extract_level(todo_item.get('class', []))
        level_prefix = '+' * level
        
        # Get description
        desc_span = todo_item.find('span', class_='description')
        description = desc_span.text.strip() if desc_span else ''
        
        # Get due date
        due_date = extract_due_date(todo_item)
        
        # Get tag
        tag = extract_tag(todo_item)
        
        # Construct todo line
        todo_line = f"{level_prefix} {description}"
        if due_date:
            todo_line += f" {due_date}"
        if tag:
            todo_line += f" :{tag}"
        
        todos.append(todo_line)
    
    return '\n'.join(todos)

def main():
    html_content = sys.stdin.read()
    todo_text = html_to_todo(html_content)
    print(todo_text)

if __name__ == "__main__":
    main()