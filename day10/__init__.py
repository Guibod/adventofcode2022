from collections import defaultdict


class History(defaultdict):
    def __init__(self):
        super().__init__(lambda: {})

    @staticmethod
    def is_interesting(cycle):
        if cycle - 20 < 0:
            return False
        return (cycle - 20) % 40 == 0

    def signal_sum(self):
        return sum(v["signal"] for v in self.values())


class Clock:
    def __init__(self):
        self.cycle = 0


class Register:
    def __init__(self):
        self.X = 1


class CPU:
    def __init__(self, register: Register = None):
        self.cycle = 0
        self.register = register or Register()
        self.history = History()

    def addx(self, value):
        self.tick()
        self.tick()
        self.register.X += int(value)

    def noop(self):
        self.tick()

    def tick(self):
        self.cycle += 1
        if self.history.is_interesting(self.cycle):
            self.history[self.cycle] = {
                "X": self.register.X,
                "signal": self.register.X * self.cycle
            }

    def run(self, filename):
        with open(filename, encoding="utf-8") as file:
            for line in file.readlines():
                line = line.rstrip().split(" ")
                method = getattr(self, line[0])
                method(*line[1:])

class CRT:
    def __init__(self):
        self.register = Register()
        self.cpu = CPU(register=self.register)


test = CPU()
assert test.register.X == 1
assert test.cycle == 0

test.noop()
assert test.register.X == 1
assert test.cycle == 1

test.addx(3)
assert test.register.X == 4
assert test.cycle == 3

test.addx(-5)
assert test.register.X == -1
assert test.cycle == 5

test_cpu = CPU()
test_cpu.run("test.txt")
assert test_cpu.history[20]["X"] == 21
assert test_cpu.history[20]["signal"] == 420
assert test_cpu.history[60]["X"] == 19
assert test_cpu.history[60]["signal"] == 1140
assert test_cpu.history[100]["X"] == 18
assert test_cpu.history[100]["signal"] == 1800
assert test_cpu.history[140]["X"] == 21
assert test_cpu.history[140]["signal"] == 2940
assert test_cpu.history[180]["X"] == 16
assert test_cpu.history[180]["signal"] == 2880
assert test_cpu.history[220]["X"] == 18
assert test_cpu.history[220]["signal"] == 3960

assert test_cpu.history.signal_sum() == 13140

cpu = CPU()
cpu.run("input.txt")
print(f"The sum of signal at interesting tick is {cpu.history.signal_sum()}")