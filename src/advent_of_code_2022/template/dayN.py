from typing import List


def main() -> None:
    input = read_input("src/advent_of_code_2022/dayN/test.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(input: List[str]) -> int:
    return 0


def solve_part2(input: List[str]) -> int:
    return 0


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
