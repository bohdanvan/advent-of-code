from __future__ import annotations
from enum import Enum
from functools import reduce
import re
from typing import List, Optional, Tuple, TypeVar

from utils.utils import split_to_chunks


class Monkey:
    def __init__(
        self,
        id: int,
        init_items: List[int],
        operation: Operation,
        monkey_test: MonkeyTest,
        divider: int,
    ):
        self.id: int = id
        self.items: List[int] = init_items.copy()
        self.operation: Operation = operation
        self.monkey_test: MonkeyTest = monkey_test
        self.inspections_count = 0
        self.divider = divider
        self.mod: Optional[int] = None

    @classmethod
    def parse(cls, lines: List[str], divider: int = 3) -> Monkey:
        return Monkey(
            id=int(from_regex(r"Monkey (\d+):", lines[0])),
            init_items=[
                int(e.strip())
                for e in from_regex(r"Starting items: (.+)", lines[1]).split(",")
            ],
            operation=Operation.parse(lines[2]),
            monkey_test=MonkeyTest.parse(lines[3:6]),
            divider=divider,
        )

    def inspect(self) -> List[Tuple[int, int]]:
        res = []

        for item in self.items:
            new_item = self.operation.apply(item)
            new_item = new_item // self.divider
            if self.mod:
                new_item = new_item % self.mod
            new_monkey = self.monkey_test.run_test(new_item)

            res.append((new_monkey, new_item))

        self.inspections_count += len(self.items)
        self.items = []

        return res

    def add_item(self, item: int) -> None:
        self.items.append(item)

    def set_mod(self, mod: int) -> None:
        self.mod = mod


class OperationType(Enum):
    ADD = "+"
    MULTIPLY = "*"
    SQR = "^2"


class Operation:
    def __init__(self, type: OperationType, val: Optional[int] = None):
        self.type = type
        self.val = val

    def apply(self, n: int) -> int:
        if self.type == OperationType.ADD:
            return n + (self.val if self.val else 0)
        elif self.type == OperationType.MULTIPLY:
            return n * (self.val if self.val else 1)
        elif self.type == OperationType.SQR:
            return n * n
        else:
            raise AssertionError()

    @classmethod
    def parse(cls, s: str) -> Operation:
        op_str = from_regex(r"Operation: new = old (.+)", s)
        if op_str == "* old":
            return Operation(OperationType.SQR)

        tokens = op_str.split()
        return Operation(OperationType(tokens[0]), int(tokens[1]))


class MonkeyTest:
    def __init__(self, divider: int, positive_monkey: int, negative_monkey: int):
        self.divider = divider
        self.positive_monkey = positive_monkey
        self.negative_monkey = negative_monkey

    def run_test(self, n: int) -> int:
        if n % self.divider == 0:
            return self.positive_monkey
        else:
            return self.negative_monkey

    @classmethod
    def parse(cls, lines: List[str]) -> MonkeyTest:

        return MonkeyTest(
            divider=int(from_regex(r"Test: divisible by (\d+)", lines[0])),
            positive_monkey=int(
                from_regex(r"If true: throw to monkey (\d+)", lines[1])
            ),
            negative_monkey=int(
                from_regex(r"If false: throw to monkey (\d+)", lines[2])
            ),
        )


def from_regex(pattern: str, s: str) -> str:
    match = re.search(pattern, s.strip())
    if not match:
        raise AssertionError
    return match.group(1)


def main() -> None:
    input = read_input("src/advent_of_code_2022/day11/input.txt")

    monkeys = parse_input(input, divider=3)
    print(f"1 -> {solve_part1(monkeys, 20)}")

    monkeys_2 = parse_input(input, divider=1)
    print(f"2 -> {solve_part2(monkeys_2)}")


def parse_input(input: List[str], divider: int) -> List[Monkey]:
    return [Monkey.parse(lines, divider) for lines in split_to_chunks(input, 7)]


def solve_part1(monkeys: List[Monkey], rounds: int):
    for round in range(rounds):
        for monkey in monkeys:
            new_monkeys = monkey.inspect()

            for (new_monkey, new_item) in new_monkeys:
                monkeys[new_monkey].add_item(new_item)

    monkeys.sort(key=lambda m: m.inspections_count, reverse=True)

    return monkeys[0].inspections_count * monkeys[1].inspections_count


def solve_part2(monkeys: List[Monkey]):
    mod = reduce(lambda a, b: a * b, [m.monkey_test.divider for m in monkeys], 1)
    for m in monkeys:
        m.set_mod(mod)
    return solve_part1(monkeys, 10000)


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
