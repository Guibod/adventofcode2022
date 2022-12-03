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


class Rucksack:
    def __init__(self, content):
        p = int(len(content) / 2)
        self.comp1 = Compartment(content[:p])
        self.comp2 = Compartment(content[p:])

    @property
    def both(self):
        a = set(self.comp1)
        b = set(self.comp2)
        c = a.intersection(b)
        d = list(c)
        return d

def parse_priority(filename):
    score = 0
    with open(filename, encoding="utf-8") as file:
        for line in file:
            rucksack = Rucksack(line.strip())
            for item in rucksack.both:
                score += item.value
    return score

assert Item("a").value == 1
assert Item("z").value == 26
assert Item("A").value == 27
assert Item("Z").value == 52

s = Rucksack("vJrwpWtwJgWrhcsFMMfFFhFp")
assert s.comp1.raw == "vJrwpWtwJgWr"
assert s.comp2.raw == "hcsFMMfFFhFp"
assert s.both[0] == Item("p")

assert parse_priority("test.txt") == 157

result = parse_priority("input.txt")
print(f"Total priority for item present in both rucksack is : {result}")