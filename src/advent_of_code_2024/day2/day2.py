from typing import List

LOWER_BOUND = 1
UPPER_BOUND = 3


def main() -> None:
    lines = read_input("src/advent_of_code_2024/day2/input.txt")

    print(f"1 -> {solve_part1(lines)}")
    print(f"2 -> {solve_part2(lines)}")


def solve_part1(lines: List[str]) -> int:
    reports = parse(lines)
    return sum(1 if is_valid_report_part1(report) else 0 for report in reports)


def solve_part2(lines: List[str]) -> int:
    reports = parse(lines)
    for r in reports:
        print(f"{r}: {is_valid_report_part2(r)}")
    return sum(1 if is_valid_report_part2(report) else 0 for report in reports)


def is_valid_report_part1(a: List[int]) -> bool:
    if len(a) <= 1:
        return True

    is_asc = a[0] < a[-1]
    for i in range(1, len(a)):
        diff = a[i] - a[i - 1]
        if not is_valid_report_diff(diff, is_asc):
            return False

    return True


def is_valid_report_part2(a: List[int]) -> bool:
    if len(a) <= 2:
        return True

    ## Brute force: O(M * N)
    return any(is_valid_report_part1(a[0:i] + a[i + 1 :]) for i in range(len(a)))


def is_valid_report_diff(diff: int, is_asc: bool) -> bool:
    return (
        (diff > 0) == is_asc and abs(diff) >= LOWER_BOUND and abs(diff) <= UPPER_BOUND
    )


def parse(lines: List[str]) -> List[List[int]]:
    return [[int(e) for e in line.split()] for line in lines]


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
