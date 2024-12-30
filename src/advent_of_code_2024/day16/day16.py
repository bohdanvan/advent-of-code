from collections import defaultdict
from enum import StrEnum
from queue import PriorityQueue
from typing import Dict, List, Tuple

from more_itertools import first

from utils.utils import flatten


Board = List[str]
Pos = Tuple[int, int]


class Direction(StrEnum):
    RIGHT = ">"
    LEFT = "<"
    DOWN = "V"
    UP = "^"


DIRECTION_TO_POS_INC: Dict[Direction, Pos] = {
    Direction.RIGHT: (0, +1),
    Direction.LEFT: (0, -1),
    Direction.DOWN: (+1, 0),
    Direction.UP: (-1, 0),
}

OPPOSITE_DIRECTION: Dict[Direction, Direction] = {
    Direction.RIGHT: Direction.LEFT,
    Direction.LEFT: Direction.RIGHT,
    Direction.DOWN: Direction.UP,
    Direction.UP: Direction.DOWN,
}


def main() -> None:
    input = read_input("src/advent_of_code_2024/day16/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(board: Board) -> int:
    score, _ = find_best_paths(board)
    return score


def solve_part2(board: Board) -> int:
    _, paths = find_best_paths(board)
    unique_pos = set(flatten(paths))
    return len(unique_pos)


def find_best_paths(board: Board) -> Tuple[int, List[List[Pos]]]:
    visited: Dict[Tuple[Pos, Direction], int] = defaultdict(int)

    start_pos = find_pos(board, "S")
    end_pos = find_pos(board, "E")

    moves_pq: PriorityQueue[Tuple[int, Pos, Direction, List[Pos]]] = PriorityQueue()
    moves_pq.put((0, start_pos, Direction.LEFT, [start_pos]))

    final_paths: List[Tuple[int, List[Pos]]] = []

    while not moves_pq.empty():
        score, (i, j), direction, path = moves_pq.get()

        if (i, j) == end_pos:
            final_paths.append((score, path))
            continue

        if ((i, j), direction) in visited and score > visited[((i, j), direction)]:
            continue

        visited[((i, j), direction)] = score

        for next_direction, (i_inc, j_inc) in DIRECTION_TO_POS_INC.items():
            next_i, next_j = i + i_inc, j + j_inc
            if is_valid_position((next_i, next_j), board) and board[next_i][next_j] in (
                ".",
                "E",
                "S",
            ):
                next_score = score + get_score_inc(direction, next_direction)
                new_path = path + [(next_i, next_j)]
                moves_pq.put((next_score, (next_i, next_j), next_direction, new_path))

    min_score = min(score for score, _ in final_paths)
    best_paths = [path for score, path in final_paths if score == min_score]
    return (min_score, best_paths)


def is_valid_position(pos: Pos, board: List[str]) -> bool:
    i, j = pos
    return i >= 0 and i < len(board) and j >= 0 and j < len(board[i])


def get_score_inc(curr_direction: Direction, next_direction: Direction) -> int:
    if (
        next_direction == curr_direction
        or next_direction == OPPOSITE_DIRECTION[curr_direction]
    ):
        return 1
    else:
        return 1000 + 1


def find_pos(board: Board, cell: str) -> Pos:
    return first(
        (i, j)
        for i in range(len(board))
        for j in range(len(board[0]))
        if board[i][j] == cell
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
