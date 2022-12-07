from typing import List


def main() -> None:
    input = read_input(
        "src/advent_of_code_2022/day6/input.txt"
    )

    print(f"1 -> {solve_part1(input, 4)}")
    print(f"2 -> {solve_part1(input, 14)}")


def solve_part1(s: str, seq_len: int):
    for i in range(seq_len, len(s)):
        if not has_duplicates(s[i-seq_len:i]):
            return i
    return -1


def has_duplicates(s: str):
    return len({ch for ch in s}) < len(s)


def solve_part2():
    pass


def read_input(file_name: str) -> str:
    with open(file_name) as f:
        return f.readline().strip()


if __name__ == "__main__":
    main()
