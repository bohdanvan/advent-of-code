from collections import defaultdict
from typing import Dict, List, Set, Tuple, TypedDict


class PuzzleInput(TypedDict):
    orders: List[Tuple[int, ...]]
    update_lists: List[List[int]]


def main() -> None:
    matrix = read_input("src/advent_of_code_2024/day5/input.txt")

    print(f"1 -> {solve_part1(matrix)}")
    print(f"2 -> {solve_part2(matrix)}")


def solve_part1(input: List[str]) -> int:
    puzzle_input = parse_intput(input)
    orders = to_struct_orders(puzzle_input["orders"])

    return sum(
        update_list[len(update_list) // 2]
        for update_list in puzzle_input["update_lists"]
        if is_valid_update_list(update_list, orders)
    )


def to_struct_orders(order: List[Tuple[int, ...]]) -> Dict[int, Set[int]]:
    res: Dict[int, Set[int]] = defaultdict(lambda: set())

    for left, right in order:
        res[left].add(right)

    return res


def is_valid_update_list(update_list: List[int], orders: Dict[int, Set[int]]) -> bool:
    for i in range(len(update_list)):
        for j in range(i + 1, len(update_list)):
            left = update_list[i]
            right = update_list[j]
            if left in orders[right]:
                return False

    return True


def solve_part2(input: List[str]) -> int:
    puzzle_input = parse_intput(input)
    orders = to_struct_orders(puzzle_input["orders"])

    invalid_update_lists = [
        update_list
        for update_list in puzzle_input["update_lists"]
        if not is_valid_update_list(update_list, orders)
    ]
    valid_lists = [
        make_valid_update_list(update_list, orders)
        for update_list in invalid_update_lists
    ]

    return sum(update_list[len(update_list) // 2] for update_list in valid_lists)


def make_valid_update_list(
    update_list: List[int], orders: Dict[int, Set[int]]
) -> List[int]:
    filtered_orders: Dict[int, Set[int]] = defaultdict(lambda: set())
    for i in range(len(update_list) - 1):
        for j in range(i + 1, len(update_list)):
            a, b = update_list[i], update_list[j]

            if b in orders[a]:
                filtered_orders[a].add(b)

            if a in orders[b]:
                filtered_orders[b].add(a)

    page_to_count = [(right, len(lefts)) for right, lefts in filtered_orders.items()]
    page_to_count.sort(key=lambda p: p[1], reverse=True)
    return [p[0] for p in page_to_count]


def parse_intput(input: List[str]) -> PuzzleInput:
    input_break = input.index("")
    return PuzzleInput(
        orders=[tuple(map(int, row.split("|")[0:2])) for row in input[0:input_break]],
        update_lists=[
            list(map(int, row.split(","))) for row in input[input_break + 1 :]
        ],
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
