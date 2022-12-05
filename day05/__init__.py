import re
from collections import defaultdict


class Procedure:
    pattern = re.compile(r'move (?P<quantity>\d+) from (?P<source>\d+) to (?P<target>\d+)')

    def __init__(self, quantity, source, target):
        self.quantity = int(quantity)
        self.source = int(source) - 1
        self.target = int(target) - 1

    @classmethod
    def parse(cls, string):
        match = cls.pattern.search(string)
        if not match:
            raise ValueError

        return cls(match.group("quantity"), match.group("source"), match.group("target"))


class Crate:
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return self.content == other

    def __repr__(self):
        return f"[{self.content}]"


class Stack(list):
    pass


class Cargo:
    pattern = re.compile(r'(?P<crate>\[(?P<content>\w)])')

    def __init__(self):
        self.stacks = defaultdict(lambda: Stack())

    def parse_line(self, string):
        one_match = self.pattern.search(string)
        if not one_match:
            raise ValueError

        for i, col in enumerate(range(0, len(string), 4)):
            match = self.pattern.match(string[col:col+3])
            if match:
                self.stacks[i].insert(0, Crate(match.group("content")))

    def apply(self, p: Procedure):
        for i in range(p.quantity):
            self.stacks[p.target].append(self.stacks[p.source][-1])
            self.stacks[p.source].pop()

    def top(self):
        out = " " * (len(self.stacks))
        for k, v in self.stacks.items():
            try:
                top = v[-1].content
            except IndexError:
                top = " "
            out = out[:k] + top + out[k+1:]
        return out


def parse_file(filename):
    cargo = Cargo()
    procedure = []
    with open(filename, encoding="utf-8") as file:
        for line in file:
            try:
                try:
                    cargo.parse_line(line)
                except ValueError:
                    procedure.append(Procedure.parse(line))
            except ValueError:
                pass

    return cargo, procedure


cargo, procedure = parse_file("test.txt")
assert len(procedure) == 4
assert procedure[0].source == 1
assert procedure[0].target == 0
assert procedure[0].quantity == 1

assert len(cargo.stacks) == 3
assert len(cargo.stacks[0]) == 2
assert cargo.stacks[0][1] == "N"
assert cargo.stacks[0][0] == "Z"
assert len(cargo.stacks[1]) == 3
assert cargo.stacks[1][2] == "D"
assert cargo.stacks[1][1] == "C"
assert cargo.stacks[1][0] == "M"
assert len(cargo.stacks[2]) == 1
assert cargo.stacks[2][0] == "P"

cargo.apply(procedure[0])
assert len(cargo.stacks[0]) == 3
assert cargo.stacks[0][2] == "D"
assert cargo.stacks[0][1] == "N"
assert cargo.stacks[0][0] == "Z"
assert len(cargo.stacks[1]) == 2
assert cargo.stacks[1][1] == "C"
assert cargo.stacks[1][0] == "M"
assert len(cargo.stacks[2]) == 1
assert cargo.stacks[2][0] == "P"

cargo.apply(procedure[1])
assert len(cargo.stacks[0]) == 0
assert len(cargo.stacks[1]) == 2
assert cargo.stacks[1][1] == "C"
assert cargo.stacks[1][0] == "M"
assert len(cargo.stacks[2]) == 4
assert cargo.stacks[2][3] == "Z"
assert cargo.stacks[2][2] == "N"
assert cargo.stacks[2][1] == "D"
assert cargo.stacks[2][0] == "P"

cargo.apply(procedure[2])
cargo.apply(procedure[3])
assert cargo.top() == "CMZ"

cargo, procedure = parse_file("input.txt")
for p in procedure:
    cargo.apply(p)
print(f"Top most crates after procedure are encoded as : {cargo.top()}")