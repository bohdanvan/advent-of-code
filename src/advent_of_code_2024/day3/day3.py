from operator import mul
import re
from typing import List, Tuple

LOWER_BOUND = 1
UPPER_BOUND = 3


def main() -> None:
    input = read_input("src/advent_of_code_2024/day3/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(input: str) -> int:
    return sum(
        pair[0] * pair[1]
        for pair in [parse_mutliplier(mult_str) for mult_str in find_multipliers(input)]
    )


def find_multipliers(input: str) -> List[str]:
    return re.findall(r"mul\(\d+,\d+\)", input)


def solve_part2(input: str) -> int:
    instructions = find_instructions(input)

    res = 0
    mul_enabled = True
    for instruction in instructions:
        if instruction == "don't":
            mul_enabled = False
        elif instruction == "do":
            mul_enabled = True
        else:
            if mul_enabled:
                pair = parse_mutliplier(instruction)
                res += pair[0] * pair[1]

    return res


def parse_mutliplier(input: str) -> Tuple[int, int]:
    res = re.findall(r"\d+", input)
    return (int(res[0]), int(res[1]))


def find_instructions(input: str) -> List[str]:
    return re.findall(r"mul\(\d+,\d+\)|don\'t|do", input)


def read_input(file_name: str) -> str:
    with open(file_name) as f:
        return f.read()


if __name__ == "__main__":
    main()
