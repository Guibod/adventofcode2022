class Section:
    def __init__(self, low, high):
        self.low = int(low)
        self.high = int(high)

    def fully_contains(self, section):
        return self.low <= section.low <= self.high and self.low <= section.high <= self.high

    def overlaps(self, section):
        r = range(max(self.low, section.low), min(self.high, section.high) + 1)
        return len(r) > 0


class Assignment:
    def __init__(self, input):
        str_section = input.strip().split(",")
        self.section1 = Section(*str_section[0].split("-"))
        self.section2 = Section(*str_section[1].split("-"))

    def has_fully_contains(self):
        return self.section1.fully_contains(self.section2) or self.section2.fully_contains(self.section1)

    def has_overlap(self):
        return self.section1.overlaps(self.section2)

assert Section(2,8).fully_contains(Section(3,7))
assert Section(4,6).fully_contains(Section(6,6))
assert Assignment("2-4,6-8").section1.low == 2
assert Assignment("2-4,6-8").section1.high == 4
assert Assignment("2-4,6-8").section2.low == 6
assert Assignment("2-4,6-8").section2.high == 8
assert Section(5,7).overlaps(Section(7,9)) is True
assert Section(2,8).overlaps(Section(3,7)) is True
assert Section(6,6).overlaps(Section(4,6)) is True
assert Section(2,6).overlaps(Section(4,8)) is True
assert Section(2,6).overlaps(Section(4,8)) is True
assert Section(1,10).overlaps(Section(11,20)) is False


def count_fully_contains(filename):
    count = 0
    with open(filename, encoding="utf-8") as file:
        for line in file:
            if Assignment(line).has_fully_contains():
                count += 1
    return count

def count_overlaps(filename):
    count = 0
    with open(filename, encoding="utf-8") as file:
        for line in file:
            if Assignment(line).has_overlap():
                count += 1
    return count


assert count_fully_contains("test.txt") == 2
assert count_overlaps("test.txt") == 4

count = count_fully_contains("input.txt")
print(f"There are {count} assignment having one section that fully contains another")

count = count_overlaps("input.txt")
print(f"There are {count} assignment having one section overlapping another")