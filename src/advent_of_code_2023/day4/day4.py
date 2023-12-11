import re
from typing import List, Tuple


def main() -> None:
    lines = read_input("src/advent_of_code_2023/day4/input.txt")
    input = parse(lines)

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def parse(lines: List[str]) -> List[Tuple[List[int], List[int]]]:
    return [parse_line(line) for line in lines]


def parse_line(line: str) -> Tuple[List[int], List[int]]:
    match = re.search(r"^Card[\s\d]*: ([\s\d]*) \| ([\s\d]*)$", line.strip())
    if not match:
        raise AssertionError(f"Doesn't match a pattern: {line}")
    return (
        [int(part) for part in match.group(1).strip().split()],
        [int(part) for part in match.group(2).strip().split()],
    )


def solve_part1(input: List[Tuple[List[int], List[int]]]) -> int:
    return sum(winning_score(winning, hand) for winning, hand in input)


def solve_part2(input: List[Tuple[List[int], List[int]]]):
    cards_count = {i: 1 for i in range(len(input))}

    for i, (winning, hand) in enumerate(input):
        matched_cards = count_matched_cards(winning, hand)
        for j in range(i + 1, i + matched_cards + 1):
            cards_count[j] += cards_count[i]

    return sum(cards_count.values())


def winning_score(winning: List[int], hand: List[int]) -> int:
    matched_cards = count_matched_cards(winning, hand)
    return 2 ** (matched_cards - 1) if matched_cards > 0 else 0


def count_matched_cards(winning: List[int], hand: List[int]) -> int:
    return len(set(winning) & set(hand))


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
