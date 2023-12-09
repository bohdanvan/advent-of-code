from functools import reduce
from typing import Dict, List, Set, Tuple


def main() -> None:
    lines = read_input("src/advent_of_code_2023/day3/input.txt")

    print(f"1 -> {solve_part1(lines)}")
    print(f"2 -> {solve_part2(lines)}")


def solve_part1(matrix: List[str]) -> int:
    sum = 0
    curr_num = 0
    is_curr_valid = False

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j].isdigit():
                curr_num = curr_num * 10 + int(matrix[i][j])
                if not is_curr_valid:
                    is_curr_valid = any(
                        [
                            is_symbol(matrix, x, y)
                            for x, y in create_neighbour_idxs(i, j)
                        ]
                    )
            else:
                if is_curr_valid:
                    sum += curr_num
                curr_num = 0
                is_curr_valid = False

        if is_curr_valid:
            sum += curr_num
        curr_num = 0
        is_curr_valid = False

    return sum


def solve_part2(matrix: List[str]) -> int:
    gear_dict: Dict[Tuple[int, int], Set[int]] = {}

    curr_num = 0
    curr_gears: Set[Tuple[int, int]] = set()

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j].isdigit():
                curr_num = curr_num * 10 + int(matrix[i][j])
                neighbour_idxs = create_neighbour_idxs(i, j)
                gears = set(
                    (x, y) for x, y in neighbour_idxs if is_star_symbol(matrix, x, y)
                )
                curr_gears.update(gears)
            else:
                for x, y in curr_gears:
                    if (x, y) not in gear_dict:
                        gear_dict[(x, y)] = set()
                    gear_dict[(x, y)].add(curr_num)
                curr_num = 0
                curr_gears = set()

        for x, y in curr_gears:
            if (x, y) not in gear_dict:
                gear_dict[(x, y)] = set()
            gear_dict[(x, y)].add(curr_num)
        curr_num = 0
        curr_gears = set()

    gear_sum = 0
    for nums in gear_dict.values():
        if len(nums) == 2:
            gear_sum += reduce((lambda x, y: x * y), nums)

    return gear_sum


def create_neighbour_idxs(i: int, j: int) -> List[Tuple[int, int]]:
    return [
        (i - 1, j - 1),
        (i - 1, j),
        (i - 1, j + 1),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j - 1),
        (i + 1, j),
        (i + 1, j + 1),
    ]


def is_valid_idx(matrix: List[str], i: int, j: int) -> bool:
    return i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix[i])


def is_symbol(matrix: List[str], i: int, j: int) -> bool:
    if is_valid_idx(matrix, i, j):
        return not matrix[i][j].isdigit() and matrix[i][j] != "."
    return False


def is_star_symbol(matrix: List[str], i: int, j: int) -> bool:
    if is_valid_idx(matrix, i, j):
        return matrix[i][j] == "*"
    return False


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
