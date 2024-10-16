import json
import os

# class for a single task with an id, title, and completion status
class Task:
    def __init__(self, id, title, completed=False):
        self.id = id  # unique identifier for the task
        self.title = title  # title for the  task
        self.completed = completed # status indicating whether the task is complete or not

    def __repr__(self):
        # string representation of the task for display, showing completed status
        status = "✓" if self.completed else "✗"  # mark as completed or not
        return f"{self.id}. {self.title} [{status}]"

# global task list and file
tasks = []  # list to store all task
task_file = "tasks.json"  # JSON file
next_task_id = 1  # to assign next task id

def add_task(title):
    # adding a new task with the provided task title
    global next_task_id
    tasks.append(Task(next_task_id, title))  # add new task to the list
    next_task_id += 1  # increase the task id for next task

def view_tasks():
    # display all tasks or notify if no tasks exist
    if tasks:
        for task in tasks:
            print(task)  # print each task
    else:
        print("No tasks available.") # notify if there no tasks

def delete_task(task_id):
    # remove a task by its id
    global tasks
    tasks = [task for task in tasks if task.id != task_id]  # keep tasks that don't match the id

def complete_task(task_id):
    # mark a task as complete by its id
    for task in tasks:
        if task.id == task_id:
            task.completed = True  # update task status as completed
            return
    print(f"Task {task_id} not found.")# notify if the task id does not exists

def save_tasks():
    # save all tasks to a JSON file
    with open(task_file, 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)  # save tasks as dictionaries and write to the JSON file


def load_tasks():
    # load tasks from a JSON file if it exists
    global tasks, next_task_id
    if os.path.exists(task_file): # check is the task file exists
        with open(task_file, 'r') as f:
            tasks = [Task(**t) for t in json.load(f)]  # recreate task objects from JSON
        next_task_id = max([task.id for task in tasks], default=0) + 1  # set next task id

def cli():
    # command-line interface for interacting with tasks
    load_tasks()  # load tasks from the file at startup

    while True:
        print("\n1: Add | 2: View | 3: Delete | 4: Complete | 5: Save | 6: Exit")
        cmd = input("Enter your Task: ").strip().lower()# get user input for the command

        if cmd in ["1", "add"]:
            task_title = input("Enter task title: ").strip() # prompt for task title
            if task_title:
                add_task(task_title)  # add task if title is provided
            else:
                print("Task title cannot be empty.") # notify if title is empty
        elif cmd in ["2", "view"]:
            view_tasks()  # display all tasks
        elif cmd in ["3", "delete"]:
            try:
                task_id = int(input("Enter task ID to delete: ").strip()) # get task id
                delete_task(task_id)  # delete the task by provided id
            except ValueError:
                print("Invalid input. Please enter a valid task ID.") # notify is input is invalid
        elif cmd in ["4", "complete"]:
            try:
                task_id = int(input("Enter task ID to complete: ").strip()) # get task id
                complete_task(task_id) # marks the task as completed
            except ValueError:
                print("Invalid input. Please enter a valid task ID.") # notify is input is invalid
        elif cmd in ["5", "save"]:
            save_tasks()  # save tasks to file
        elif cmd in ["6", "exit"]:
            save_tasks()  # save and exit
            break # exit the loop
        else:
            print("Invalid choice. Please select a valid option.") # notify the choice is invalid

if __name__ == "__main__":
    cli()  # run the task manager
