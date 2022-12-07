import re
from typing import List

class Node:
    def __init__(self, name):
        self.name = str(name)
        self.parent = None
        self.children = []

    @property
    def path(self):
        if self.parent:
            return self.parent.path + "/" + self.name
        return ""

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

    def directories(self, min_size=None, max_size=None):
        for child in self.children:
            if isinstance(child, Directory):
                yield from child.directories(min_size, max_size)

        if min_size is not None and getattr(self, "size") <= min_size:
            return
        if max_size is not None and getattr(self, "size") >= max_size:
            return

        yield self


class Directory(Node):
    @property
    def size(self):
        return sum(node.size for node in self.children)

class File(Node):
    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

file_result = re.compile(r"((?P<size>\d+)|dir) (?P<name>\w+)")
def parser(filename):
    root = Directory("")
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
assert len(test_root["a"]) == 4
assert len(test_root["a"]["e"]) == 1
assert len(test_root["a"]["e"]) == 1
assert test_root["a"]["e"].size == 584
assert test_root["a"].size == 94853
assert test_root["d"].size == 24933642
assert test_root.size == 48381165

MAX_SIZE = 100000
test_large_dirs = list(test_root.directories(max_size=100000))
print(test_large_dirs)
assert len(test_large_dirs) == 2
assert test_root.size == 48381165

tree = parser("input.txt")
small_dirs = list(tree.directories(max_size=MAX_SIZE))
total_size = sum(d.size for d in small_dirs)
print(f"There are {len(small_dirs)} directories "
      f"with content at most {MAX_SIZE}, for a total of {total_size}")

DISK_SIZE = 70000000
REQUIRED_FREE = 30000000
missing_space = REQUIRED_FREE - (DISK_SIZE - tree.size)
print(f"As we use {tree.size}, and require at least {REQUIRED_FREE}, "
      f"we should free at least {missing_space}")
large_dirs = list(tree.directories(min_size=missing_space))
sorted_large_dirs = sorted(large_dirs, key=lambda x: x.size)
smallest_of_the_largest = sorted_large_dirs[0]
print(f"The directory we should delete is {smallest_of_the_largest.path}, "
      f"with a size of {smallest_of_the_largest.size}")
