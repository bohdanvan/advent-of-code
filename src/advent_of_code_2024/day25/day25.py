from dataclasses import dataclass
from enum import StrEnum
from itertools import product
from typing import List

from utils.utils import split_list

Board = List[str]


class SchemaType(StrEnum):
    LOCK = "LOCK"
    KEY = "KEY"


@dataclass
class Schema:
    type: SchemaType
    heights: List[int]


def main() -> None:
    input = read_input("src/advent_of_code_2024/day25/input.txt")

    print(f"1 -> {solve_part1(input)}")


def solve_part1(input: List[str]) -> int:
    boards = parse(input)
    schemas = [to_schema(board) for board in boards]
    locks = [s for s in schemas if s.type == SchemaType.LOCK]
    keys = [s for s in schemas if s.type == SchemaType.KEY]
    max_height = len(boards[0]) - 2

    return sum(
        1 for lock, key in product(locks, keys) if is_match(lock, key, max_height)
    )


def is_match(lock: Schema, key: Schema, max_height: int) -> bool:
    res = all(
        lock_height + key_height <= max_height
        for lock_height, key_height in zip(lock.heights, key.heights)
    )
    return res


def to_schema(board: Board) -> Schema:
    if board[0][0] == "#":
        return Schema(
            SchemaType.LOCK,
            build_heights(board),
        )
    else:
        return Schema(
            SchemaType.KEY,
            build_heights(board),
        )


def build_heights(board: Board) -> List[int]:
    return list(map(lambda row: row.count("#"), rotate(board[1:-1])))


def rotate(matrix: List[str]) -> List[List[str]]:
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]


def parse(input: List[str]) -> List[Board]:
    return split_list(input, "")


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
