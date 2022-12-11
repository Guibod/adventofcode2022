import logging
import math
import uuid
from functools import reduce, lru_cache
from typing import List
import petname
from colorama import Fore, Style

RUN_TEST = True
DEBUG = False

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')
if DEBUG:
    logger.setLevel(logging.DEBUG)


class Human:
    STYLE = f"{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}"

    def __init__(self, troop: 'Troop'):
        self.horde = troop
        self.name = "Narrator"

    def un_stress(self, item: 'Item'):
        item.worry = int(math.floor(item.worry / 3))
        logger.debug("Worry level is divided by 3 to %s.", (self, item.worry))

    def __str__(self):
        return f"Human {self.STYLE}{self.name}{Style.NORMAL}"

    def __repr__(self):
        return f"Human {self.name}"


class StressedHuman(Human):
    def un_stress(self, item: 'Item'):
        item.worry %= horde.super_modulo
        logger.debug("Worry level is normalized by super-modulo of %d to %s.",
                     horde.super_modulo, item.worry)


class Item:
    STYLE = f"{Style.BRIGHT}{Fore.BLUE}"

    def __init__(self, value):
        self.unique_id = str(uuid.uuid4().fields[-1])[:5]
        self.worry = int(value)

    def __repr__(self):
        return f"Item {self.unique_id} ({self.worry})"

    def __str__(self):
        return f"Item {Item.STYLE}{self.unique_id}{Style.RESET_ALL} ({self.worry})"


class Monkey:
    STYLE = f"{Style.BRIGHT}{Fore.GREEN}"

    def __init__(self, troop: 'Troop'):
        self.horde = troop
        self.index = len(troop.monkeys)
        self.name = petname.adjective()
        self.divisible_by = None
        self.monkey_true = None
        self.monkey_false = None
        self.items = []
        self.operation_operator = "+"
        self.operation_value = 0
        self.turns = 0

    def __repr__(self):
        return f"Monkey {self.index} ({self.name}{Style.RESET_ALL})"

    def __str__(self):
        return f"Monkey {self.index} ({Monkey.STYLE}{self.name}{Style.RESET_ALL})"

    def handle_without_care(self, item: Item):
        new = item.worry
        if self.operation_operator == "+":
            new = item.worry + int(self.operation_value)
        elif self.operation_operator == "*" and self.operation_value == "old":
            new = pow(item.worry, 2)
        elif self.operation_operator == "*":
            new = item.worry * int(self.operation_value)
        item.worry = new
        logger.debug("    New worry level is %s.", Fore.GREEN + str(item.worry) + Style.RESET_ALL)

    def get_bored_with(self, item: Item):
        logger.debug("    %s gets bored with %s.", self, item)
        self.items.remove(item)
        if item.worry % self.divisible_by == 0:
            logger.debug("    Current worry level is divisible by %d", self.divisible_by)
            target = self.horde[self.monkey_true]
            target.items.append(item)
            logger.debug("    %s is thrown to %s.", item, target)
        else:
            logger.debug("    Current worry level is NOT divisible by %d", self.divisible_by)
            target = self.horde[self.monkey_false]
            target.items.append(item)
            logger.debug("    %s is thrown to %s.", item, target)

    def turn(self, item: Item):
        self.turns += 1
        logger.debug("  %s inspects %s", self, item)
        self.handle_without_care(item)
        self.horde.human.un_stress(item)
        self.get_bored_with(item)

    def round(self):
        logger.debug("%s", self)
        for item in list(self.items):
            self.turn(item)


class Troop:
    def __init__(self, human: Human = None):
        self.monkeys: List[Monkey] = []
        self.round_index = 0
        self.human = human or Human(self)

    def __getitem__(self, index: int) -> Monkey:
        return self.monkeys[index]

    @property
    @lru_cache(maxsize=10)
    def super_modulo(self):
        return reduce(lambda x, y: x * y,
                      [monkey.divisible_by for monkey in self.monkeys])

    @classmethod
    def parse(cls, filename):
        parsed_troop = cls()
        with open(filename, encoding="utf-8") as file:
            for line in file.readlines():
                if line.startswith("Monkey "):
                    parsed_troop.monkeys.append(Monkey(parsed_troop))
                elif line.startswith("  Starting items:"):
                    items = [Item(item.strip())
                             for item
                             in line.rstrip().split(":")[-1].split(",")]
                    parsed_troop[-1].items = items
                elif line.startswith("  Operation: new = "):
                    operator, value = line.rstrip().split(" ")[-2::]
                    parsed_troop[-1].operation_operator = operator
                    parsed_troop[-1].operation_value = value
                elif line.startswith("  Test: divisible by "):
                    number = line.rstrip().split(" ")[-1]
                    parsed_troop[-1].divisible_by = int(number)
                elif line.startswith("    If true: throw to monkey "):
                    number = line.rstrip().split(" ")[-1]
                    parsed_troop[-1].monkey_true = int(number)
                elif line.startswith("    If false: throw to monkey "):
                    number = line.rstrip().split(" ")[-1]
                    parsed_troop[-1].monkey_false = int(number)

        return parsed_troop

    def wait(self, rounds=1):
        logging.debug("Waiting %s rounds...", Fore.CYAN + str(rounds) + Style.RESET_ALL)
        for _ in range(0, rounds):
            self.round()

    def round(self):
        monkey: Monkey

        self.round_index += 1
        if self.round_index % 100 == 0:
            logging.info("Starting round %s",
                         Fore.CYAN + str(self.round_index) + Style.RESET_ALL)
        else:
            logging.debug("Starting round %s",
                          Fore.CYAN + str(self.round_index) + Style.RESET_ALL)

        for monkey in self.monkeys:
            monkey.round()

    def monkey_business_score(self):
        turns = [monkey.turns for monkey in horde.monkeys]
        top2 = sorted(turns, reverse=True)[:2]
        return top2[0] * top2[1]


if RUN_TEST:
    observed_item = Item(10)
    test_monkey = Monkey(Troop())
    test_monkey.operation_value = "19"
    test_monkey.operation_operator = "*"
    test_monkey.handle_without_care(observed_item)
    assert observed_item.worry == 190

    horde = Troop.parse("test.txt")
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

    horde = Troop.parse("test.txt")
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

horde = Troop.parse("input.txt")
horde.wait(20)
print(f"The monkey business score after {horde.round_index} "
      f"rounds is {Fore.MAGENTA}{Style.BRIGHT}{horde.monkey_business_score()}{Style.RESET_ALL}")

if RUN_TEST:
    horde = Troop.parse("test.txt")
    horde.human = StressedHuman(horde)

    horde.round()
    assert horde.round_index == 1
    assert [monkey.turns for monkey in horde] == [2, 4, 3, 6]

    horde.wait(19)
    assert horde.round_index == 20
    assert [monkey.turns for monkey in horde] == [99, 97, 8, 103]

    horde.wait(980)
    assert horde.round_index == 1000
    assert [monkey.turns for monkey in horde] == [5204, 4792, 199, 5192]

    horde.wait(9000)
    assert horde.round_index == 10000
    assert [monkey.turns for monkey in horde] == [52166, 47830, 1938, 52013]

    assert horde.monkey_business_score() == 2713310158

horde = Troop.parse("input.txt")
horde.human = StressedHuman(horde)
horde.wait(10000)
logger.setLevel(logging.INFO)
print(f"The monkey business score after {horde.round_index} rounds, "
      f"{Fore.RED}{Style.BRIGHT}with a stressed human{Style.RESET_ALL}, "
      f"is {Fore.MAGENTA}{Style.BRIGHT}{horde.monkey_business_score()}{Style.RESET_ALL}")
