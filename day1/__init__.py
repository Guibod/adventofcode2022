class Elf:
    def __init__(self, name):
        self.name = name
        self.bag = Bag()


class Bag(list):
    @property
    def calories(self):
        return sum(self)


elves = []

with open('input.txt') as fp:
    elves.append(Elf("Elf #1"))
    for line in fp:
        try:
            elves[-1].bag.append(int(line.strip()))
        except ValueError:
            elves.append(Elf("Elf #" + str(len(elves) + 1)))

elf_top_calory = sorted(elves, key=lambda x: x.bag.calories, reverse=True)[0]
print(f"{elf_top_calory.name} is the elf with the most calories ({elf_top_calory.bag.calories})")

top_3_elves = sorted(elves, key=lambda x: x.bag.calories, reverse=True)[:3]
print("Top 3 calorie hoarders:")
for elf in top_3_elves:
    print(f" - {elf_top_calory.name} ({elf_top_calory.bag.calories})")

top_3_calories = sum([elf.bag.calories for elf in top_3_elves])
print(f"That’s a total of {top_3_calories}")
