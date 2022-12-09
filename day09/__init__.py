from enum import Enum
from typing import Tuple, List


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other: 'Position') -> int:
        return max(abs(other.x - self.x), abs(other.y - self.y))

    def follow(self, other: 'Position') -> 'Position':
        x_new = self.x
        y_new = self.y
        if self.distance(other) > 1:
            x_delta = other.x - self.x
            if x_delta:
                x_new += int(x_delta / abs(x_delta))
            y_delta = other.y - self.y
            if y_delta:
                y_new += int(y_delta / abs(y_delta))

        return Position(x_new, y_new)

    @property
    def coords(self) -> Tuple[int, int]:
        return self.x, self.y

    def __eq__(self, other):
        return self.coords == other

    def __hash__(self):
        return hash(self.coords)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __copy__(self):
        return Position(self.x, self.y)


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    RIGHT = "R"
    LEFT = "L"


class Knot:
    def __init__(self, name="H", pos: 'Position' = None):
        self.name = name
        self.pos = pos or Position(0, 0)
        self.history = [self.pos.coords]
        self.attached = None

    def attach(self, knot: 'Knot'):
        self.attached = knot

    def __repr__(self):
        return f"{self.name} {self.pos}"

    def move(self, position: Position):
        self.pos = position
        self.history.append(position.coords)

        if self.attached:
            next_pos = self.attached.pos
            self.attached.move(next_pos.follow(self.pos))

    def apply_order(self, direction: Direction, distance: int):
        for _ in range(distance):
            pos = self.pos
            if direction == Direction.UP.value:
                pos.y += 1
            elif direction == Direction.DOWN.value:
                pos.y -= 1
            elif direction == Direction.RIGHT.value:
                pos.x += 1
            elif direction == Direction.LEFT.value:
                pos.x -= 1
            self.move(pos)


class Rope(list):
    def __init__(self, length=1):
        super().__init__()
        self.append(Knot("H"))

        if length <= 1:
            raise ValueError("Rope must at least be of length 1")

        for i in enumerate(range(length - 1), start=1):
            knot = Knot(str(i))
            self[-1].attach(knot)
            self.append(knot)

    @property
    def head(self) -> Knot:
        return self[0]

    @property
    def tail(self) -> Knot:
        return self[-1]

    def _apply(self, instructions: List[Tuple[Direction, int]]):
        for direction, distance in instructions:
            self.head.apply_order(direction, distance)

    def apply(self, filename):
        self._apply(self.parse(filename))

    @classmethod
    def parse(cls, filename):
        instructions = []
        with open(filename, encoding="utf-8") as file:
            for line in file.readlines():
                direction, distance = line.split(" ", maxsplit=2)
                instructions.append((direction, int(distance)))
        return instructions


assert Position(0, 0).distance(Position(1, 1)) == 1
assert Position(0, 0).distance(Position(2, 1)) == 2
assert Position(0, 0).distance(Position(2, 2)) == 2

assert Position(0, 0).follow(Position(0, 0)) == (0, 0)
assert Position(0, 0).follow(Position(1, 0)) == (0, 0)
assert Position(0, 0).follow(Position(2, 0)) == (1, 0)
assert Position(0, 0).follow(Position(-2, 0)) == (-1, 0)
assert Position(0, 0).follow(Position(0, 0)) == (0, 0)
assert Position(0, 0).follow(Position(0, 1)) == (0, 0)
assert Position(0, 0).follow(Position(0, 2)) == (0, 1)
assert Position(0, 0).follow(Position(0, -2)) == (0, -1)
assert Position(0, 0).follow(Position(2, 2)) == (1, 1)
assert Position(0, 0).follow(Position(2, 1)) == (1, 1)
assert Position(0, 0).follow(Position(1, 2)) == (1, 1)
assert Position(0, 0).follow(Position(-1, -2)) == (-1, -1)

test_rope = Rope(2)
test_instructions = Rope.parse("test.txt")

test_rope.head.apply_order(*test_instructions[0])
assert test_rope.head.pos == (4, 0)
assert test_rope.tail.pos == (3, 0)

test_rope.head.apply_order(*test_instructions[1])
assert test_rope.head.pos == (4, 4)
assert test_rope.tail.pos == (4, 3)

test_rope.head.apply_order(*test_instructions[2])
assert test_rope.head.pos == (1, 4)
assert test_rope.tail.pos == (2, 4)

test_rope.head.apply_order(*test_instructions[3])
assert test_rope.head.pos == (1, 3)
assert test_rope.tail.pos == (2, 4)

test_rope.head.apply_order(*test_instructions[4])
assert test_rope.head.pos == (5, 3)
assert test_rope.tail.pos == (4, 3)

test_rope.head.apply_order(*test_instructions[5])
assert test_rope.head.pos == (5, 2)
assert test_rope.tail.pos == (4, 3)

test_rope.head.apply_order(*test_instructions[6])
assert test_rope.head.pos == (0, 2)
assert test_rope.tail.pos == (1, 2)

test_rope.head.apply_order(*test_instructions[7])
assert test_rope.head.pos == (2, 2)
assert test_rope.tail.pos == (1, 2)

assert len(set(test_rope.tail.history)) == 13

rope = Rope(2)
rope.apply("input.txt")

visited = len(set(rope.tail.history))
print(f"A rope of 2, the tail visited {visited} distinct positions")

test_rope_2 = Rope(10)
test_rope_2.apply("test.larger.txt")
visited = len(set(test_rope_2.tail.history))
assert visited == 36

rope2 = Rope(10)
rope2.apply("input.txt")
visited = len(set(rope2.tail.history))
print(f"A rope of 10, the tail visited {visited} distinct positions")
