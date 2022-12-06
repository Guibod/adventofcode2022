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


class CrateMover9000:
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


class CrateMover9001(CrateMover9000):
    def apply(self, p: Procedure):
        section = self.stacks[p.source][-p.quantity:]
        del self.stacks[p.source][-p.quantity:]
        self.stacks[p.target].extend(section)


def parse_file(cratemover, filename):
    procedure = []
    with open(filename, encoding="utf-8") as file:
        for line in file:
            try:
                try:
                    cratemover.parse_line(line)
                except ValueError:
                    procedure.append(Procedure.parse(line))
            except ValueError:
                pass

    return procedure


test_mover_9000 = CrateMover9000()
procedure = parse_file(test_mover_9000, "test.txt")
assert len(procedure) == 4
assert procedure[0].source == 1
assert procedure[0].target == 0
assert procedure[0].quantity == 1

assert len(test_mover_9000.stacks) == 3
assert len(test_mover_9000.stacks[0]) == 2
assert test_mover_9000.stacks[0][1] == "N"
assert test_mover_9000.stacks[0][0] == "Z"
assert len(test_mover_9000.stacks[1]) == 3
assert test_mover_9000.stacks[1][2] == "D"
assert test_mover_9000.stacks[1][1] == "C"
assert test_mover_9000.stacks[1][0] == "M"
assert len(test_mover_9000.stacks[2]) == 1
assert test_mover_9000.stacks[2][0] == "P"

test_mover_9000.apply(procedure[0])
assert len(test_mover_9000.stacks[0]) == 3
assert test_mover_9000.stacks[0][2] == "D"
assert test_mover_9000.stacks[0][1] == "N"
assert test_mover_9000.stacks[0][0] == "Z"
assert len(test_mover_9000.stacks[1]) == 2
assert test_mover_9000.stacks[1][1] == "C"
assert test_mover_9000.stacks[1][0] == "M"
assert len(test_mover_9000.stacks[2]) == 1
assert test_mover_9000.stacks[2][0] == "P"

test_mover_9000.apply(procedure[1])
assert len(test_mover_9000.stacks[0]) == 0
assert len(test_mover_9000.stacks[1]) == 2
assert test_mover_9000.stacks[1][1] == "C"
assert test_mover_9000.stacks[1][0] == "M"
assert len(test_mover_9000.stacks[2]) == 4
assert test_mover_9000.stacks[2][3] == "Z"
assert test_mover_9000.stacks[2][2] == "N"
assert test_mover_9000.stacks[2][1] == "D"
assert test_mover_9000.stacks[2][0] == "P"

test_mover_9000.apply(procedure[2])
test_mover_9000.apply(procedure[3])
assert test_mover_9000.top() == "CMZ"


test_mover_9001 = CrateMover9001()
procedure = parse_file(test_mover_9001, "test.txt")

test_mover_9001.apply(procedure[0])
assert len(test_mover_9001.stacks[0]) == 3
assert test_mover_9001.stacks[0][2] == "D"
assert test_mover_9001.stacks[0][1] == "N"
assert test_mover_9001.stacks[0][0] == "Z"
assert len(test_mover_9001.stacks[1]) == 2
assert test_mover_9001.stacks[1][1] == "C"
assert test_mover_9001.stacks[1][0] == "M"
assert len(test_mover_9001.stacks[2]) == 1
assert test_mover_9001.stacks[2][0] == "P"

test_mover_9001.apply(procedure[1])
assert len(test_mover_9001.stacks[0]) == 0
assert len(test_mover_9001.stacks[1]) == 2
assert test_mover_9001.stacks[1][1] == "C"
assert test_mover_9001.stacks[1][0] == "M"
assert len(test_mover_9001.stacks[2]) == 4
assert test_mover_9001.stacks[2][3] == "D"
assert test_mover_9001.stacks[2][2] == "N"
assert test_mover_9001.stacks[2][1] == "Z"
assert test_mover_9001.stacks[2][0] == "P"

test_mover_9001.apply(procedure[2])
assert len(test_mover_9001.stacks[0]) == 2
assert test_mover_9001.stacks[0][1] == "C"
assert test_mover_9001.stacks[0][0] == "M"
assert len(test_mover_9001.stacks[1]) == 0
assert len(test_mover_9001.stacks[2]) == 4
assert test_mover_9001.stacks[2][3] == "D"
assert test_mover_9001.stacks[2][2] == "N"
assert test_mover_9001.stacks[2][1] == "Z"
assert test_mover_9001.stacks[2][0] == "P"

test_mover_9001.apply(procedure[3])
assert len(test_mover_9001.stacks[0]) == 1
assert test_mover_9001.stacks[0][0] == "M"
assert len(test_mover_9001.stacks[1]) == 1
assert test_mover_9001.stacks[1][0] == "C"
assert len(test_mover_9001.stacks[2]) == 4
assert test_mover_9001.stacks[2][3] == "D"
assert test_mover_9001.stacks[2][2] == "N"
assert test_mover_9001.stacks[2][1] == "Z"
assert test_mover_9001.stacks[2][0] == "P"

assert test_mover_9001.top() == "MCD"

crate_mover_9000 = CrateMover9000()
procedure = parse_file(crate_mover_9000, "input.txt")
for p in procedure:
    crate_mover_9000.apply(p)
print(f"Top most crates for a CrateMover 9000 after procedure are encoded as : {crate_mover_9000.top()}")

crate_mover_9001 = CrateMover9001()
procedure = parse_file(crate_mover_9001, "input.txt")
for p in procedure:
    crate_mover_9001.apply(p)
print(f"Top most crates for a CrateMover 9001 after procedure are encoded as : {crate_mover_9001.top()}")