import logging
import math
import uuid
from typing import List
import petname
from colorama import Fore, Style

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


class Item:
    def __init__(self, value):
        self.id = str(uuid.uuid4().fields[-1])[:5]
        self.worry = int(value)

    def __repr__(self):
        return f"Item {self.id} ({self.worry})"

    def __str__(self):
        return f"Item {Fore.BLUE}{self.id}{Style.RESET_ALL} ({self.worry})"


class Monkey:
    def __init__(self, horde: 'Horde', index: int = None, name: str = None, divisible_by: int = 0,
                 monkey_true: int = None, monkey_false: int = None,
                 items: List[Item] = list):
        self.horde = horde
        self.index = index or len(horde.monkeys)
        self.name = name or petname.adjective()
        self.divisible_by = divisible_by
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.items = items
        self.operation_operator = "+"
        self.operation_value = 0
        self.turns = 0

    def __repr__(self):
        return f"Monkey {self.index} ({self.name}{Style.RESET_ALL})"

    def __str__(self):
        return f"Monkey {self.index} ({Fore.GREEN}{Style.BRIGHT}{self.name}{Style.RESET_ALL})"

    def handle_without_care(self, item: Item):
        new = item.worry
        if self.operation_operator == "+":
            new = item.worry + int(self.operation_value)
        elif self.operation_operator == "*" and self.operation_value == "old":
            new = pow(item.worry, 2)
        elif self.operation_operator == "*":
            new = item.worry * int(self.operation_value)
        item.worry = new
        logger.debug(f"    New worry level is {Fore.GREEN}{item.worry}{Style.RESET_ALL}.")

    def get_bored_with(self, item: Item):
        item.worry = int(math.floor(item.worry / 3))
        logger.debug(f"    {self} gets bored with {item}. Worry level is divided by 3 to {Fore.GREEN}{item.worry}{Style.RESET_ALL}.")
        self.items.remove(item)
        if item.worry % self.divisible_by == 0:
            logger.debug(f"    Current worry level is divisible by {Fore.GREEN}{self.divisible_by}{Style.RESET_ALL}.")
            target = self.horde[self.monkey_true]
            target.items.append(item)
            logger.debug(f"    {item} is thrown to {target}.")
        else:
            logger.debug(f"    Current worry level is {Fore.RED}not{Style.RESET_ALL} divisible by {Fore.GREEN}{self.divisible_by}{Style.RESET_ALL}.")
            target = self.horde[self.monkey_false]
            target.items.append(item)
            logger.debug(f"    {item} is thrown to {target}.")

    def turn(self, item: Item):
        self.turns += 1
        logger.debug(f"  {self} inspects an item with a worry level of {Fore.GREEN}{item.worry}{Style.RESET_ALL}.")
        self.handle_without_care(item)
        self.get_bored_with(item)

    def round(self):
        logger.debug(f"{self}:")
        for item in list(self.items):
            self.turn(item)


class Horde:
    def __init__(self):
        self.monkeys: List[Monkey] = []
        self.round_index = 0

    def __getitem__(self, index: int) -> Monkey:
        return self.monkeys[index]

    @classmethod
    def parse(cls, filename):
        horde = cls()
        with open(filename, encoding="utf-8") as file:
            for line in file.readlines():
                if line.startswith("Monkey "):
                    horde.monkeys.append(Monkey(horde))
                elif line.startswith("  Starting items:"):
                    items = [Item(item.strip())
                             for item
                             in line.rstrip().split(":")[-1].split(",")]
                    horde[-1].items = items
                elif line.startswith("  Operation: new = "):
                    operator, value = line.rstrip().split(" ")[-2::]
                    horde[-1].operation_operator = operator
                    horde[-1].operation_value = value
                elif line.startswith("  Test: divisible by "):
                    number = line.rstrip().split(" ")[-1]
                    horde[-1].divisible_by = int(number)
                elif line.startswith("    If true: throw to monkey "):
                    number = line.rstrip().split(" ")[-1]
                    horde[-1].monkey_true = int(number)
                elif line.startswith("    If false: throw to monkey "):
                    number = line.rstrip().split(" ")[-1]
                    horde[-1].monkey_false = int(number)

        return horde

    def wait(self, round=1):
        for _ in range(0, round):
            self.round()

    def round(self):
        monkey: Monkey
        for monkey in self.monkeys:
            monkey.round()
        self.round_index += 1

    def monkey_business_score(self):
        turns = [monkey.turns for monkey in horde.monkeys]
        top2 = sorted(turns, reverse=True)[:2]
        return top2[0] * top2[1]


observed_item = Item(10)
test_monkey = Monkey(Horde())
test_monkey.operation_value = "19"
test_monkey.operation_operator = "*"
test_monkey.handle_without_care(observed_item)
assert observed_item.worry == 190

horde = Horde.parse("test.txt")
assert len(horde.monkeys) == 4
assert len(horde[0].items) == 2
assert horde[0].items[0].worry == 79
assert horde[0].items[1].worry == 98
assert horde[0].divisible_by == 23
assert horde[0].monkey_true == 2
assert horde[0].monkey_false == 3

observed_monkey = horde[0]
observed_item = observed_monkey.items[0]
observed_monkey.turn(observed_item)
assert len(observed_monkey.items) == 1
assert observed_item in horde[3].items
assert observed_item.worry == 500

observed_item = observed_monkey.items[0]
observed_monkey.turn(observed_item)
assert len(observed_monkey.items) == 0
assert observed_item in horde[3].items
assert observed_item.worry == 620

assert len(horde[1].items) == 4
horde[1].round()
assert len(horde[1].items) == 0


horde = Horde.parse("test.txt")
horde.round()
assert horde.round_index == 1
assert [item.worry for item in horde[0].items] == [20, 23, 27, 26]
assert [item.worry for item in horde[1].items] == [2080, 25, 167, 207, 401, 1046]
assert [item.worry for item in horde[2].items] == []
assert [item.worry for item in horde[3].items] == []

horde.round()
assert horde.round_index == 2
assert [item.worry for item in horde[0].items] == [695, 10, 71, 135, 350]
assert [item.worry for item in horde[1].items] == [43, 49, 58, 55, 362]
assert [item.worry for item in horde[2].items] == []
assert [item.worry for item in horde[3].items] == []

horde.round()
assert horde.round_index == 3
assert [item.worry for item in horde[0].items] == [16, 18, 21, 20, 122]
assert [item.worry for item in horde[1].items] == [1468, 22, 150, 286, 739]
assert [item.worry for item in horde[2].items] == []
assert [item.worry for item in horde[3].items] == []

horde.round()
assert horde.round_index == 4
assert [item.worry for item in horde[0].items] == [491, 9, 52, 97, 248, 34]
assert [item.worry for item in horde[1].items] == [39, 45, 43, 258]
assert [item.worry for item in horde[2].items] == []
assert [item.worry for item in horde[3].items] == []

horde.round()
assert horde.round_index == 5
assert [item.worry for item in horde[0].items] == [15, 17, 16, 88, 1037]
assert [item.worry for item in horde[1].items] == [20, 110, 205, 524, 72]
assert [item.worry for item in horde[2].items] == []
assert [item.worry for item in horde[3].items] == []

horde.wait(15)
assert horde.round_index == 20
assert [item.worry for item in horde[0].items] == [10, 12, 14, 26, 34]
assert [item.worry for item in horde[1].items] == [245, 93, 53, 199, 115]
assert [item.worry for item in horde[2].items] == []
assert [item.worry for item in horde[3].items] == []

assert [monkey.turns for monkey in horde.monkeys] == [101, 95, 7, 105]
assert horde.monkey_business_score() == 10605

horde = Horde.parse("input.txt")
horde.wait(20)
print(f"The monkey business score is {Fore.MAGENTA}{Style.BRIGHT}{horde.monkey_business_score()}{Style.RESET_ALL}")