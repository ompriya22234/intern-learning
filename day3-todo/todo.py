import json
import sys
import os

TASK_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    with open(TASK_FILE, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(task):
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added: {task}")


def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")


def remove_task(task_number):
    tasks = load_tasks()

    if task_number < 1 or task_number > len(tasks):
        print("Task number does not exist.")
        return

    removed = tasks.pop(task_number - 1)
    save_tasks(tasks)
    print(f"Removed: {removed}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("python todo.py add <task>")
        print("python todo.py remove <number>")
        print("python todo.py list")
        return

    command = sys.argv[1]

    if command == "add":
        task = " ".join(sys.argv[2:])
        add_task(task)

    elif command == "list":
        list_tasks()

    elif command == "remove":
        try:
            number = int(sys.argv[2])
            remove_task(number)
        except (IndexError, ValueError):
            print("Please provide a valid task number.")

    else:
        print("Unknown command.")


if __name__ == "__main__":
    main()
