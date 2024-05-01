import os
import datetime

class Task:
    def __init__(self, description, priority="Normal", due_date=None, completed=False):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.description} ({self.priority}, Due: {self.due_date}, Status: {status})"


class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            return True
        return False

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            return True
        return False

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for task in self.tasks:
                file.write(f"{task.description},{task.priority},{task.due_date},{task.completed}\n")

    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    description, priority, due_date, completed = line.strip().split(',')
                    due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None
                    completed = completed == 'True'
                    self.tasks.append(Task(description, priority, due_date, completed))

    def display_tasks(self):
        if not self.tasks:
            print("No tasks found.")
        else:
            for i, task in enumerate(self.tasks):
                print(f"{i + 1}. {task}")


def get_date_input(prompt):
    while True:
        date_str = input(prompt)
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            return date
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")


def main():
    todo_list = TodoList()
    filename = "tasks.txt"
    todo_list.load_from_file(filename)

    while True:
        print("\n===== To-Do List =====")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Remove Task")
        print("4. View Tasks")
        print("5. Save and Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            priority = input("Enter priority (Low/Normal/High): ").capitalize()
            due_date = get_date_input("Enter due date (YYYY-MM-DD), leave empty if none: ")
            todo_list.add_task(Task(description, priority, due_date))

        elif choice == "2":
            todo_list.display_tasks()
            index = int(input("Enter the task number to mark as completed: ")) - 1
            if todo_list.mark_task_completed(index):
                print("Task marked as completed.")
            else:
                print("Invalid task number.")

        elif choice == "3":
            todo_list.display_tasks()
            index = int(input("Enter the task number to remove: ")) - 1
            if todo_list.remove_task(index):
                print("Task removed successfully.")
            else:
                print("Invalid task number.")

        elif choice == "4":
            todo_list.display_tasks()

        elif choice == "5":
            todo_list.save_to_file(filename)
            print("Tasks saved. Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
