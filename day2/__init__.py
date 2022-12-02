from enum import Enum


class Outcome(Enum):
    WIN = 6
    DRAW = 3
    LOSS = 0

    @classmethod
    def factory_2(cls, input):
        if input in ['X']:
            return cls.LOSS
        if input in ['Y']:
            return cls.DRAW
        if input in ['Z']:
            return cls.WIN
        raise TypeError(f"{input} should be either: X, Y or Z")


class Play(Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

    def __lt__(self, other):
        diff = self.value - other.value
        if diff in [-1, 2]:
            return True
        return False

    def __gt__(self, other):
        diff = self.value - other.value
        if diff in [1, -2]:
            return True
        return False

    def check(self, other):
        if self > other:
            return Outcome.WIN
        if self < other:
            return Outcome.LOSS
        return Outcome.DRAW

    @classmethod
    def factory_1(cls, input):
        if input in ['A', 'X']:
            return cls.ROCK
        if input in ['B', 'Y']:
            return cls.PAPER
        if input in ['C', 'Z']:
            return cls.SCISSOR
        raise TypeError(f"{input} should be either: A, B, C, X, Y or Z")


def compute_phase1(filename):
    score = 0
    with open(filename) as fp:
        for line in fp:
            theirs, ours = map(Play.factory_1, line.strip().split(" ", 2))

            result = ours.check(theirs)
            score += result.value + ours.value

    return score

def compute_phase2(filename):
    score = 0

    with open(filename) as fp:
        for line in fp:
            line = line.strip().split(" ", 2)
            theirs = Play.factory_1(line[0])
            outcome = Outcome.factory_2(line[1])

            if Play.ROCK.check(theirs) == outcome:
                ours = Play.ROCK
            elif Play.PAPER.check(theirs) == outcome:
                ours = Play.PAPER
            else:
                ours = Play.SCISSOR

            score += outcome.value + ours.value

    return score


assert(Play.SCISSOR > Play.PAPER)
assert(Play.PAPER > Play.ROCK)
assert(Play.ROCK > Play.SCISSOR)
assert(Play.PAPER < Play.SCISSOR)
assert(Play.ROCK < Play.PAPER)
assert(Play.SCISSOR < Play.ROCK)
assert(Play.ROCK == Play.ROCK)
assert(Play.PAPER == Play.PAPER)
assert(Play.SCISSOR == Play.SCISSOR)

test_expected = 15
test_computed = compute_phase1('test.txt')
assert test_computed == test_expected, f"Validation failed for phase 1, computed {test_computed} instead of {test_expected}"

real = compute_phase1("input.txt")
print(f"Computed score in phase1: {real}")

test_expected = 12
test_computed = compute_phase2('test.txt')
assert test_computed == test_expected, f"Validation failed for phase 2, computed {test_computed} instead of {test_expected}"

real = compute_phase2("input.txt")
print(f"Computed score in phase2: {real}")