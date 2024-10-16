import json
import os


# Task class
class Task:
    def __init__(self, id, title, completed=False):
        self.id = id
        self.title = title
        self.completed = completed

    def __repr__(self):
        status = "✓" if self.completed else "✗"
        return f"{self.id}. {self.title} [{status}]"


# Task Manager functions
tasks = []
task_file = "tasks.json"
next_task_id = 1


def add_task(title):
    """Adds a new task to the list."""
    global next_task_id
    tasks.append(Task(next_task_id, title))
    next_task_id += 1
    print(f"Task '{title}' added.")


def view_tasks():
    """Displays all tasks, or notifies if there are no tasks."""
    if tasks:
        for task in tasks:
            print(task)
    else:
        print("No tasks available.")


def delete_task(task_id):
    """Deletes a task by ID."""
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    print(f"Task {task_id} deleted.") if tasks else print(f"Task {task_id} not found.")


def complete_task(task_id):
    """Marks a task as complete by ID."""
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            print(f"Task {task_id} marked as complete.")
            return
    print(f"Task {task_id} not found.")


def save_tasks():
    """Saves tasks to a JSON file."""
    with open(task_file, 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)
    print("Tasks saved to file.")


def load_tasks():
    """Loads tasks from a JSON file, if available."""
    global tasks, next_task_id
    if os.path.exists(task_file):
        with open(task_file, 'r') as f:
            tasks = [Task(**t) for t in json.load(f)]
        next_task_id = max([task.id for task in tasks], default=0) + 1
        print("Tasks loaded from file.")
    else:
        print("No saved tasks found.")


# Enhanced CLI to handle both words and numbers
def cli():
    """Command-Line Interface to interact with the task manager."""
    load_tasks()

    while True:
        print("\n1: Add | 2: View | 3: Delete | 4: Complete | 5: Save | 6: Exit")
        cmd = input("> ").strip().lower()

        if cmd in ["1", "add"]:
            task_title = input("Enter task title: ").strip()
            if task_title:
                add_task(task_title)
            else:
                print("Task title cannot be empty.")
        elif cmd in ["2", "view"]:
            view_tasks()
        elif cmd in ["3", "delete"]:
            try:
                task_id = int(input("Enter task ID to delete: ").strip())
                delete_task(task_id)
            except ValueError:
                print("Invalid input. Please enter a valid task ID.")
        elif cmd in ["4", "complete"]:
            try:
                task_id = int(input("Enter task ID to complete: ").strip())
                complete_task(task_id)
            except ValueError:
                print("Invalid input. Please enter a valid task ID.")
        elif cmd in ["5", "save"]:
            save_tasks()
        elif cmd in ["6", "exit"]:
            save_tasks()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    cli()
