from typing import List


def main() -> None:
    input = read_input(
        "/Users/bvanchuhov/Projects/Python/algo-py/src/advent_of_code_2022/dayN/test.txt"
    )

    print(f"1 -> {solve_part1()}")
    print(f"2 -> {solve_part2()}")


def solve_part1():
    pass


def solve_part2():
    pass


def read_input(file_name: str) -> List[List[str]]:
    with open(file_name) as f:
        return [line.split() for line in f]


if __name__ == "__main__":
    main()
