class Item:
    """
    An item found in the elve’s rucksacks.
    An item is described by a letter, and has a value of 1 to 52 depending on the associated letter

    As usual, we provide comparison methods for equality (__eq__), sort (__lt__) and hashing since
    we are using a LOT of set intersection that don’t compare equality but uses hash comparison instead
    """
    def __init__(self, letter):
        self.letter = letter

    @property
    def priority(self):
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
    """
    A rucksack sub-content (eg compartiment)
    Will cast content from string to Item
    """
    def __init__(self, content):
        self.raw = content
        super().__init__(sorted([Item(letter) for letter in content]))

    @property
    def set(self):
        return set(self)


class Rucksack:
    def __init__(self, content):
        pivot = int(len(content) / 2)
        self.comp1 = Compartment(content[:pivot])
        self.comp2 = Compartment(content[pivot:])
        self.all = Compartment(content)

    @property
    def common_in_both_compartments(self):
        return list(self.comp1.set.intersection(self.comp2.set))


def individual_common_items_priority_accumulator(filename):
    score = 0
    with open(filename, encoding="utf-8") as file:
        for line in file:
            rucksack = Rucksack(line.strip())
            for item in rucksack.common_in_both_compartments:
                score += item.priority
    return score


def groups_common_priority_accumulator(filename):
    score = 0
    with open(filename, encoding="utf-8") as file:
        for line in file:
            elf1 = Rucksack(line.strip()).all.set
            elf2 = Rucksack(next(file).strip()).all.set
            elf3 = Rucksack(next(file).strip()).all.set

            for common in elf1.intersection(elf2).intersection(elf3):
                score += common.priority

    return score


assert Item("a").priority == 1
assert Item("z").priority == 26
assert Item("A").priority == 27
assert Item("Z").priority == 52

s = Rucksack("vJrwpWtwJgWrhcsFMMfFFhFp")
assert s.comp1.raw == "vJrwpWtwJgWr"
assert s.comp2.raw == "hcsFMMfFFhFp"
assert s.common_in_both_compartments[0] == Item("p")

assert individual_common_items_priority_accumulator("test.txt") == 157
assert groups_common_priority_accumulator("test2.txt") == 70

result = individual_common_items_priority_accumulator("input.txt")
print(f"Total priority for item present in both rucksack is : {result}")

result = groups_common_priority_accumulator("input.txt")
print(f"Total priority for common item present in 3 elfs groups is : {result}")
