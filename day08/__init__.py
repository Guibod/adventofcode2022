from typing import List, Union
from colorama import Fore
from colorama import Style


class Tree:
    def __init__(self, grid, pos: (int, int), size: int):
        self.grid = grid
        self.x = pos[0]
        self.y = pos[1]
        self.size = int(size)

    def __eq__(self, size):
        return self.size == size

    def __gt__(self, size):
        return self.size > size

    def __lt__(self, size):
        return self.size < size

    def print(self):
        if self.visible:
            print(f"{Fore.GREEN}{Style.BRIGHT}{self.size}{Style.RESET_ALL}", end="")
        else:
            print(f"{Fore.RED}{self.size}{Style.RESET_ALL}", end="")


    @property
    def visible(self):
        if self.x in [0, self.grid.x - 1]:
            return True

        if self.y in [0, self.grid.y - 1]:
            return True

        return self.size > max([t.size for t in self.north], default=0) \
               or self.size > max([t.size for t in self.south], default=0) \
               or self.size > max([t.size for t in self.west], default=0)\
               or self.size > max([t.size for t in self.east], default=0)

    @property
    def north(self):
        return [self.grid[self.x, y] for y in reversed(range(0, self.y))]

    @property
    def south(self):
        return [self.grid[self.x, y] for y in range(self.y+1, self.grid.y)]

    @property
    def west(self):
        return [self.grid[x, self.y] for x in reversed(range(0, self.x))]

    @property
    def east(self):
        return [self.grid[x, self.y] for x in range(self.x+1, self.grid.x)]


class Grid:
    grid: List[List[Union[Tree, None]]]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = [[None]*x for _ in range(y)]

    def add(self, pos: (int, int), size: int):
        self.grid[pos[0]][pos[1]] = Tree(self, pos, size)

    def __getitem__(self, item):
        return self.grid[item[0]][item[1]]

    def visibles(self):
        for row in self.grid:
            for tree in row:
                if tree.visible:
                    yield tree

    @classmethod
    def read(cls, filename):
        dimx = dimy = 0
        with open(filename, encoding="utf-8") as file:
            for x, line in enumerate(file.readlines()):
                dimx = max(x+1, dimx)
                for y, char in enumerate(line.strip()):
                    dimy = max(y+1, dimy)
        grid = cls(dimx, dimy)

        with open(filename, encoding="utf-8") as file:
            for y, line in enumerate(file.readlines()):
                for x, char in enumerate(line.strip()):
                    grid.add((x, y), int(char))
        return grid

    def print(self):
        for row in self.grid:
            for tree in row:
                tree.print()
            print("")


test_grid = Grid.read("test.txt")
assert test_grid[3, 1] == 1
assert test_grid[3, 1].north[0] == 7
assert test_grid[3, 1].south[0] == 3
assert test_grid[3, 1].south[1] == 4
assert test_grid[3, 1].south[2] == 9
assert test_grid[3, 1].west[0] == 5
assert test_grid[3, 1].west[1] == 5
assert test_grid[3, 1].west[2] == 2
assert test_grid[3, 1].east[0] == 2

assert test_grid[0, 0] == 3
assert test_grid[0, 0].visible
assert test_grid[1, 1] == 5
assert test_grid[1, 1].visible
assert test_grid[2, 1] == 5
assert test_grid[2, 1].visible
assert test_grid[3, 1] == 1
assert not test_grid[3, 1].visible
assert test_grid[1, 2] == 5
assert test_grid[1, 2].visible
assert test_grid[2, 2] == 3
assert not test_grid[2, 2].visible
assert test_grid[3, 2] == 3
assert test_grid[3, 2].visible
assert test_grid[2, 3] == 5
assert test_grid[2, 3].visible
assert not test_grid[1, 3].visible
assert not test_grid[3, 3].visible

print("Test plot")
test_grid.print()

visibles = list(test_grid.visibles())
assert len(list(test_grid.visibles())) == 21

print("Input plot")
grid = Grid.read("input.txt")
grid.print()
visible_nb = len(list(grid.visibles()))
print(f"There are {visible_nb} trees visible in the field")