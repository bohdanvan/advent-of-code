from enum import Enum
from typing import List, Optional, TypedDict


class ReflectionType(Enum):
    VERTICAL = 1
    HORIZONTAL = 100


class Reflection(TypedDict):
    idx: int
    type: ReflectionType


GLOBAL_IDX: int = 0


def main() -> None:
    input = read_input("src/advent_of_code_2023/day13/input.txt")
    boards = split_list(input, "")

    print(f"1 -> {solve_part1(boards)}")
    print(f"2 -> {solve_part2(boards)}")


def solve_part1(boards: List[List[str]]) -> int:
    reflections = [find_all_reflections(board)[0] for board in boards]
    return sum(r["idx"] * r["type"].value for r in reflections if r is not None)


def solve_part2(boards: List[List[str]]) -> int:
    reflections = [find_reflection_with_smudge(board) for board in boards]
    return sum(r["idx"] * r["type"].value for r in reflections if r is not None)


def find_reflection_with_smudge(board: List[str]) -> Optional[Reflection]:
    original_reflection = find_all_reflections(board)[0]
    if original_reflection is None:
        return None

    global GLOBAL_IDX
    debug_ops = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            debug_ops += 1
            fixed_board = replace_smudge(board, i, j)
            reflections = find_all_reflections(fixed_board)
            new_reflections = [r for r in reflections if r != original_reflection]
            if len(new_reflections) > 1:
                raise AssertionError("Multiple new reflections")

            if len(new_reflections) == 1:
                return new_reflections[0]

    raise AssertionError("New reflections not found")


def replace_smudge(board: List[str], i: int, j: int) -> List[str]:
    return (
        board[0:i]
        + [board[i][0:j] + opposite_symbol(board[i][j]) + board[i][j + 1 :]]
        + board[i + 1 :]
    )


def opposite_symbol(s: str) -> str:
    return "#" if s == "." else "."


def find_all_reflections(board: List[str]) -> List[Reflection]:
    all_horizontal_reflection_idx = [
        Reflection(idx=idx, type=ReflectionType.HORIZONTAL)
        for idx in find_all_horizontal_reflection_idx(board)
    ]

    all_vertical_reflection_idx = [
        Reflection(idx=idx, type=ReflectionType.VERTICAL)
        for idx in find_all_vertical_reflection_idx(board)
    ]

    return all_horizontal_reflection_idx + all_vertical_reflection_idx


def find_all_horizontal_reflection_idx(board: List[str]) -> List[int]:
    res = []

    for i in range(1, len(board) // 2 + 1):
        left = board[0:i]
        right = board[i : 2 * i][::-1]
        if left == right:
            res.append(i)

    for i in range(len(board) // 2 + 1, len(board)):
        right = board[i : len(board)]
        left = board[2 * i - len(board) : i][::-1]
        if right == left:
            res.append(i)

    return res


def find_all_vertical_reflection_idx(board: List[str]) -> List[int]:
    return find_all_horizontal_reflection_idx(transpose(board))


def transpose(board: List[str]) -> List[str]:
    return [
        "".join(board[i][j] for i in range(len(board))) for j in range(len(board[0]))
    ]


def split_list(list: List[str], separator: str) -> List[List[str]]:
    sep_idxs: List[int] = (
        [-1] + [idx for idx, s in enumerate(list) if s == separator] + [len(list)]
    )
    res: List[List[str]] = []
    for i in range(len(sep_idxs) - 1):
        res.append(list[sep_idxs[i] + 1 : sep_idxs[i + 1]])
    return res


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
