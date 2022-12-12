import logging
import math
from functools import lru_cache
from itertools import product
from typing import Dict, Iterator
from astar import AStar, Infinite
from colorama import Fore, Style, Back

RUN_TEST = True
DEBUG = True

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')
if DEBUG:
    logger.setLevel(logging.DEBUG)


class Climber(AStar):
    def __init__(self, map: 'Map'):
        super().__init__()
        self.max_positive = 1
        self.max_negative = float('-inf')
        self.map = map

    def __repr__(self):
        return "A-Star Climber"

    def heuristic_cost_estimate(self, n1: 'Square', n2: 'Square'):
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = n1.pos
        (x2, y2) = n2.pos
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1: 'Square', n2: 'Square'):
        """this method always returns 1, as two 'neighbors' are always adajcent"""
        if n2.elevation - n1.elevation > 1:
            return Infinite

        return 1

    def neighbors(self, node: 'Square'):
        return node.neighbours

    def solve(self, source=None, target=None):
        if not source:
            source = self.map.start
        if not target:
            target = self.map.top

        return list(self.astar(source, target))


class Climber2(Climber):
    def __repr__(self):
        return "A-star with no Heuristic Cost Climber"

    def heuristic_cost_estimate(self, n1: 'Square', n2: 'Square'):
        return 1


class Square:
    def __init__(self, map: 'Map', pos: (int, int),
                 elevation: int):
        self.pos = pos
        self.elevation = elevation
        self.map = map

    def __hash__(self):
        return hash(self.pos)

    def map_point(self, path):
        if self in path:
            return Back.BLACK + chr(self.elevation + 97) + Style.RESET_ALL
        return self.map.print_color(self.elevation) + chr(self.elevation + 97) + Style.RESET_ALL

    def distance(self, other: 'Square'):
        return max(abs(other.pos[0] - self.pos[0]), abs(other.pos[1] - self.pos[1]))

    def __repr__(self):
        return f"Square {self.pos} [{self.elevation}]"

    @property
    @lru_cache
    def neighbours_pos(self):
        x, y = self.pos
        north = (x, y-1)
        south = (x, y+1)
        west = (x-1, y)
        east = (x+1, y)

        return [south, north, west, east]

    @property
    def neighbours(self) -> Iterator['Square']:
        for pos in self.neighbours_pos:
            try:
                yield self.map[pos]
            except KeyError:
                pass


class Map:
    def __init__(self):
        self.grid: Dict[(int, int), Square] = dict()
        self.start: Square = None
        self.top: Square = None
        self.width = 0
        self.height = 0

    def __getitem__(self, coords):
        return self.grid[coords]

    @classmethod
    def parse(cls, filename):
        parsed_map = Map()
        with open(filename, encoding="utf-8") as file:
            for y, line in enumerate(file.readlines()):
                for x, character in enumerate(line.strip()):
                    if character == "S":
                        elevation = 0
                    elif character == "E":
                        elevation = 26
                    else:
                        elevation = ord(character) - 97
                    square = Square(parsed_map, (x, y), elevation)
                    parsed_map.grid[(x, y)] = square
                    if character == "S":
                        parsed_map.start = square
                    if not parsed_map.top \
                        or parsed_map.top.elevation < square.elevation:
                        parsed_map.top = square

                    parsed_map.width = max(x + 1, parsed_map.width)
                parsed_map.height = max(y + 1, parsed_map.height)

        return parsed_map

    @property
    @lru_cache()
    def gradient(self):
        bcolor = [Back.WHITE, Back.GREEN, Back.YELLOW, Back.RED]
        bstyle = [Style.DIM, Style.NORMAL, Style.BRIGHT]
        fcolor = [Fore.BLACK]
        fstyle = [Style.DIM, Style.NORMAL, Style.BRIGHT]
        return list(product(bcolor, bstyle, fstyle, fcolor))

    def print_color(self, elevation):
        e = elevation
        t = self.top.elevation
        l = len(self.gradient)
        try:
            return "".join(self.gradient[math.floor(e * l / t)])
        except IndexError:
            return ""

    def print(self, path):
        for y in range(0, self.height):
            for x in range(0, self.width):
                print(self[x, y].map_point(path), end="")
            print()


if RUN_TEST:
    map = Map.parse("test.txt")
    climber = Climber(map)

    assert map.height == 5
    assert map.width == 8

    assert map.start.elevation == 0
    assert map.start.pos == (0, 0)
    assert list(map.start.neighbours) == [map[0, 1], map[1, 0]]

    assert map.top.elevation == 26
    assert map.top.pos == (5, 2)
    assert list(map.top.neighbours) == [map[5, 3], map[5, 1], map[4, 2], map[6, 2]]

    path = climber.solve()
    assert len(path) == 32
    assert path[0] == map[(0, 0)]
    assert path[1] == map[(1, 0)]
    assert path[2] == map[(2, 0)]
    assert path[-2] == map[(4, 2)]
    assert path[-1] == map[(5, 2)]

    assert list(map[0, 3].neighbours) == [map[0, 4], map[0, 2], map[1, 3]]

map = Map.parse("input.txt")

climber = Climber(map)
path = set(climber.solve())
map.print(path)
print(f"{climber} moved {len(path)-1} squares, to reach {map.top}")

climber2 = Climber2(map)
path3 = set(climber2.solve())
map.print(path3)
print(f"{climber2} moved {len(set(path3))-1} squares, to reach {map.top}")

