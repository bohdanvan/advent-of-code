import re
from typing import Dict, List, Tuple, TypedDict
from functools import reduce


CARD_TO_RANK_PART_1 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

CARD_TO_RANK_PART_2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


def main() -> None:
    lines = read_input("src/advent_of_code_2023/day7/input.txt")
    hands = [(parts[0], int(parts[1])) for parts in [line.split(" ") for line in lines]]

    print(f"1 -> {solve_part1(hands)}")
    print(f"2 -> {solve_part2(hands)}")


def solve_part1(hands: List[Tuple[str, int]]) -> int:
    hands.sort(key=lambda h: (primary_rank_part1(h[0]), secondary_rank_part1(h[0])))

    return sum((i + 1) * hand[1] for i, hand in enumerate(hands))


def primary_rank_part1(hand: str) -> int:
    count_dict: Dict[str, int] = dict()
    for card in hand:
        count_dict[card] = count_dict.get(card, 0) + 1

    counts = sorted(count_dict.values(), reverse=True)

    if counts[0] == 5:
        return 6
    if counts[0] == 4:
        return 5
    if counts[0] == 3 and counts[1] == 2:
        return 4
    if counts[0] == 3:
        return 3
    if counts[0] == 2 and counts[1] == 2:
        return 2
    if counts[0] == 2:
        return 1

    return 0


def secondary_rank_part1(hand: str) -> List[int]:
    return [CARD_TO_RANK_PART_1[card] for card in hand]


def solve_part2(hands: List[Tuple[str, int]]) -> int:
    hands.sort(key=lambda h: (primary_rank_part2(h[0]), secondary_rank_part2(h[0])))

    return sum((i + 1) * hand[1] for i, hand in enumerate(hands))


def primary_rank_part2(hand: str) -> int:
    count_dict: Dict[str, int] = dict()
    for card in hand:
        count_dict[card] = count_dict.get(card, 0) + 1

    jokers = count_dict.get("J", 0)
    count_dict["J"] = 0

    counts = sorted(count_dict.values(), reverse=True)

    if counts[0] + jokers == 5:
        return 6
    if counts[0] + jokers == 4:
        return 5
    if counts[0] + jokers == 3 and counts[1] == 2:
        return 4
    if counts[0] + jokers == 3:
        return 3
    if counts[0] + jokers == 2 and counts[1] == 2:
        return 2
    if counts[0] + jokers == 2:
        return 1

    return 0


def secondary_rank_part2(hand: str) -> List[int]:
    return [CARD_TO_RANK_PART_2[card] for card in hand]


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
