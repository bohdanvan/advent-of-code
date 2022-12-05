from enum import Enum, IntEnum
from typing import List, Tuple, TypeAlias

Range = Tuple[int, int]


def main() -> None:
    pairs = read_input(
        "/Users/bvanchuhov/Projects/Python/algo-py/src/advent_of_code_2022/day4/input.txt"
    )

    print(f"1 -> {solve_part1(pairs)}")
    print(f"2 -> {solve_part2(pairs)}")


def solve_part1(pairs: List[Tuple[Range, Range]]) -> int:
    return sum(
        [
            int(
                does_fully_contain(pair[0], pair[1])
                or does_fully_contain(pair[1], pair[0])
            )
            for pair in pairs
        ]
    )


def does_fully_contain(outer: Range, inner: Range) -> bool:
    return outer[0] <= inner[0] and outer[1] >= inner[1]


def solve_part2(pairs: List[Tuple[Range, Range]]) -> int:
    return sum([int(is_overlap(pair[0], pair[1])) for pair in pairs])


def is_overlap(a: Range, b: Range) -> bool:
    return (a[0] <= b[0] and b[0] <= a[1]) or (b[0] <= a[0] and a[0] <= b[1])


def read_input(file_name: str) -> List[Tuple[Range, Range]]:
    with open(file_name) as f:
        return [parse_line(line.strip()) for line in f]


def parse_line(s: str) -> Tuple[Range, Range]:
    range_strs = s.split(sep=",")
    return (parse_range(range_strs[0]), parse_range(range_strs[1]))


def parse_range(s: str) -> Range:
    boundraries = s.split(sep="-")
    return (int(boundraries[0]), int(boundraries[1]))


if __name__ == "__main__":
    main()
