#!/usr/bin/env python3

import sys

TODO_FILE = "/users/jake/documents/todo_list"


def strike_through(text):
    return "\033[9m%s\033[0m" % text


class Task:
    def __init__(self, desc, completed=False):
        self.desc = desc
        self.completed = completed

    def format(self, idx):
        listing = "%d. %s" % (idx, self.desc)
        if self.completed:
            return strike_through(listing)
        return listing


class Todo:
    def __init__(self):
        self.tasks = []

    def clear(self):
        self.tasks = []

    def read(self, path):
        with open(path, "r") as f:
            contents = f.read()
            if not contents:
                return
            lines = contents.split("\n")

        for line in lines:
            if not line:
                break
            task = Task(
                desc=line[1:],
                completed=int(line[0])
            )
            self.tasks.append(task)

    def write(self, path):
        with open(path, "w+") as f:
            for task in self.tasks:
                f.write("%d%s\n" % (
                    task.completed, task.desc
                ))

    def add(self, desc):
        task = Task(desc)
        self.tasks.append(task)

    def delete(self, idx):
        del self.tasks[idx - 1]

    def complete(self, idx):
        self.tasks[idx - 1].completed = True

    def sort(self):
        self.tasks.sort(
            key=lambda t: t.desc
        )

    def print(self):
        if not self.tasks:
            print("Todo list is empty")
        else:
            for i, task in enumerate(self.tasks, 1):
                print(task.format(i))


if __name__ == "__main__":
    todo = Todo()

    try:
        todo.read(TODO_FILE)
    except FileNotFoundError:
        pass

    command = None
    args = []
    for i, arg in enumerate(sys.argv[1:]):
        if i:
            args.append(arg)
        else:
            command = arg

    if command in ("-a", "a", "add"):
        tasks = " ".join(args).split(",")
        for task in tasks:
            todo.add(task.strip())
        todo.print()
        todo.write(TODO_FILE)

    elif command in ("-d", "d", "delete"):
        indexes = []
        for arg in args:
            try:
                idx = int(arg)
            except IndexError:
                print("Invalid task number: %s" % arg)
                exit(1)
            except ValueError:
                print("Invalid input.")
                exit(1)
            if idx in indexes:
                print("Task repeated: %d", idx)
                exit(1)
            indexes.append(int(arg))
        for i, idx in enumerate(sorted(indexes)):
            todo.delete(int(arg) - i)
        todo.print()
        todo.write(TODO_FILE)

    elif command in ("-c", "c", "complete"):
        for arg in args:
            try:
                todo.complete(int(arg))
            except IndexError:
                print("Invalid task number: %s" % arg)
                exit(1)
            except ValueError:
                print("Invalid input.")
                exit(1)
        todo.print()
        todo.write(TODO_FILE)

    elif command in ("-g", "g", "get"):
        indexes = []
        try:
            for arg in args:
                idx = int(arg) - 1
                if idx > len(todo.tasks):
                    raise IndexError
                indexes.append(idx)
        except ValueError:
            print("Invalid input.")
            exit(1)
        except IndexError:
            print("Invalid task number: %s" % arg)
            exit(1)
        for idx in indexes:
            print(todo.tasks[idx].desc)

    elif command == "clear":
        todo.clear()
        todo.write(TODO_FILE)

    elif command in ("-s", "s" "sort"):
        todo.sort()
        todo.print()
        todo.write(TODO_FILE)

    else:
        todo.print()
