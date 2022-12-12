import logging
from functools import lru_cache
from typing import Dict, Iterator, List, Set
from itertools import product


RUN_TEST = False
DEBUG = True

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')
if DEBUG:
    logger.setLevel(logging.DEBUG)


class DeathTrapException(Exception):
    pass

class Climber:
    def __init__(self, map: 'Map', pos: (int, int) = None):
        self.max_positive = 1
        self.max_negative = float('-inf')
        self.map = map
        self.history: List[(int, int)] = [pos or map.start.pos]

    def __repr__(self):
        return f"Climber at {self.pos}"

    @property
    def moves(self) -> int:
        return len(self.history) - 1

    @property
    def pos(self):
        return self.history[-1]

    def move_to(self, target):
        logger.debug("%s moves to : %s", self, target)
        self.history.append(target.pos)

    def plan_to(self, target, ahead=5) -> List[Square]:
        logger.debug("%s evaluate %d next moves toward %s", self, ahead, target)
        moves = []
        while len(moves) < ahead:
            options = self.options(self.pos, target)
            if len(options) == 0:
                raise DeathTrapException()


    def walk_to(self, target, max=100):
        i = 0
        logger.debug("%s starts a walk toward %s", self, target)
        while self.pos != target.pos:
            i += 1
            if i >= max:
                print(self.history)
                raise RuntimeError(f"Climber is exhausted after {max} moves")
            self.move_to(target)

        logger.debug("%s has reached his goal", self)

    def can_climb(self, diff):
        return self.max_negative <= diff <= self.max_positive

    def accessible(self, square: 'Square'):
        for neighbour in square.neighbours():
            diff = neighbour.elevation - square.elevation
            if neighbour.pos[0] != square.pos[0] and neighbour.pos[1] != square.pos[1]:
                # Diagonal
                continue

            if self.can_climb(diff):
                yield neighbour

    def options(self, source: (int, int), target: (int, int)):
        if source == target:
            return [target.pos]

        options = []
        for option in self.accessible(self.map[source]):
            if option.pos in self.history:
                continue  # cannot go back
            options.append(option)

        return sorted(options, key=lambda x: (x.distance(target), x.height_difference(target)))


class Square:
    def __init__(self, map: 'Map', pos: (int, int),
                 elevation: int):
        self.pos = pos
        self.elevation = elevation
        self.map = map

    def __hash__(self):
        return hash(self.pos)

    def distance(self, other: 'Square'):
        return max(abs(other.pos[0] - self.pos[0]), abs(other.pos[1] - self.pos[1]))

    def height_difference(self, other: 'Square'):
        return other.elevation - self.elevation

    def

    def is_deathtrap_for(self, other: 'Square', climber: Climber):
        pass

    def __repr__(self):
        return f"Square {self.pos} [{self.elevation}]"

    @property
    @lru_cache
    def neighbours_pos(self):
        x, y = self.pos
        x_s = [x for x in range(x - 1, x + 2) if 0 <= x < self.map.width]
        y_s = [y for y in range(y - 1, y + 2) if 0 <= y < self.map.height]
        return [pos for pos in product(x_s, y_s) if pos != self.pos]

    def neighbours(self) -> Iterator['Square']:
        for pos in self.neighbours_pos:
            yield self.map[pos]


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


if RUN_TEST:
    map = Map.parse("test.txt")
    climber = Climber(map)

    assert climber.pos == map.start.pos

    assert map.height == 5
    assert map.width == 8

    assert map.start.elevation == 0
    assert map.start.pos == (0, 0)
    assert map.start.neighbours_pos == [(0, 1), (1, 0), (1, 1)]
    assert [square.pos for square in climber.accessible(map.start)] == [(0, 1), (1, 0)]

    assert map.top.elevation == 26
    assert map.top.pos == (5, 2)
    assert map.top.neighbours_pos == [(4, 1), (4, 2), (4, 3), (5, 1), (5, 3), (6, 1), (6, 2), (6, 3)]
    assert len(list(climber.accessible(map.top))) == 4

    assert list(climber.accessible(map[2, 2])) == [map[1, 2], map[2, 1], map[2, 3]]

    assert climber.options(map.top) == [map[1, 0], map[0, 1]]
    assert climber.options(map[(1, 0)]) == [map[1, 0], map[0, 1]]

    climber.walk_to(map.top)
    assert climber.moves == 31

map = Map.parse("input.txt")
climber2 = Climber(map, (12, 10))
print(climber2.options(map.top))

climber = Climber(map)
climber.walk_to(map.top)
print(f"The climber moved {climber.moves}, to reach {map.top}")
