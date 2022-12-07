import re
from typing import List

class Node:
    def __init__(self, name):
        self.name = str(name)
        self.parent = None
        self.children = []

    def __len__(self):
        return len(self.children)

    def __getitem__(self, item):
        for node in self.children:
            if node.name == item:
                return node
        raise IndexError

    def add(self, other):
        if not isinstance(other, Node):
            raise ValueError
        other.parent = self
        self.children.append(other)


class Directory(Node):
    @property
    def size(self):
        return sum([node.size for node in self.children])

class File(Node):
    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

file_result = re.compile(r"((?P<size>\d+)|dir) (?P<name>\w+)")
def parser(filename):
    root = Node("/")
    current = root
    with open(filename, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("$"):
                command = line.split(" ")
                if command[1] == "cd":
                    if command[2] == "/":
                        current = root
                    elif command[2] == "..":
                        current = current.parent
                    else:
                        current = current[command[2]]
                elif command[1] == "ls":
                    pass
            else:
                size_or_dir, name = line.split(" ", 2)
                if size_or_dir == "dir":
                    current.add(Directory(name))
                else:
                    current.add(File(name, int(size_or_dir)))
    return root

test_root = parser("test.txt")
assert len(test_root) == 4
