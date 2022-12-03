class Item:
    def __init__(self, letter):
        self.letter = letter

    @property
    def value(self):
        if ord(self.letter) in range(97, 123):
            return ord(self.letter) - 96
        return ord(self.letter) - 64 + 26

    def __eq__(self, other):
        return self.letter == other.letter

    def __lt__(self, other):
        return self.letter < other.letter

    def __hash__(self):
        return hash(self.letter)


class Compartment(list):
    def __init__(self, content):
        self.raw = content
        super().__init__(sorted([Item(letter) for letter in content]))

    @property
    def set(self):
        return set(self)

class Rucksack:
    def __init__(self, content):
        p = int(len(content) / 2)
        self.comp1 = Compartment(content[:p])
        self.comp2 = Compartment(content[p:])
        self.all = Compartment(content)

    @property
    def both(self):
        return list(self.comp1.set.intersection(self.comp2.set))

def parse_overall_priority(filename):
    score = 0
    with open(filename, encoding="utf-8") as file:
        for line in file:
            rucksack = Rucksack(line.strip())
            for item in rucksack.both:
                score += item.value
    return score

def parse_groups(filename):
    score = 0
    with open(filename, encoding="utf-8") as file:
        for line in file:
            elf1 = Rucksack(line.strip()).all.set
            elf2 = Rucksack(next(file).strip()).all.set
            elf3 = Rucksack(next(file).strip()).all.set

            for common in elf1.intersection(elf2).intersection(elf3):
                score += common.value

    return score


assert Item("a").value == 1
assert Item("z").value == 26
assert Item("A").value == 27
assert Item("Z").value == 52

s = Rucksack("vJrwpWtwJgWrhcsFMMfFFhFp")
assert s.comp1.raw == "vJrwpWtwJgWr"
assert s.comp2.raw == "hcsFMMfFFhFp"
assert s.both[0] == Item("p")

assert parse_overall_priority("test.txt") == 157
assert parse_groups("test2.txt") == 70

result = parse_overall_priority("input.txt")
print(f"Total priority for item present in both rucksack is : {result}")

result = parse_groups("input.txt")
print(f"Total priority for common item present in 3 elfs groups is : {result}")