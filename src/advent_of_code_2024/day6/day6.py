from enum import Enum
from typing import Dict, List, Set, Tuple

from more_itertools import first


class Direction(Enum):
    RIGHT = ">"
    LEFT = "<"
    DOWN = "V"
    UP = "^"


Board = List[List[str]]
Position = Tuple[int, int]

DIRECTION_TO_POS_INC: Dict[Direction, Position] = {
    Direction.RIGHT: (0, +1),
    Direction.LEFT: (0, -1),
    Direction.DOWN: (+1, 0),
    Direction.UP: (-1, 0),
}

DIRECTION_ROTATION: Dict[Direction, Direction] = {
    Direction.RIGHT: Direction.DOWN,
    Direction.LEFT: Direction.UP,
    Direction.DOWN: Direction.LEFT,
    Direction.UP: Direction.RIGHT,
}

GUARD_CHAR = "^"
OBSTACLE_CHAR = "#"
VISITED_CHAR = "X"
VISITED_REPEATEDLY_CHAR = "O"
EMPTY_CHAR = "."


def main() -> None:
    board = read_input("src/advent_of_code_2024/day6/input.txt")
    print(f"1 -> {solve_part1(deep_copy_board(board))}")
    print(f"2 -> {solve_part2(deep_copy_board(board))}")


def solve_part1(board: Board) -> int:
    run_simulation(board)

    return sum(
        1
        for i in range(len(board))
        for j in range(len(board[0]))
        if board[i][j] == VISITED_CHAR
    )


def solve_part2(board: Board) -> int:
    original_board = deep_copy_board(board)
    run_simulation(board)

    # bruite force (1 min execution)
    return sum(
        1
        for i in range(len(board))
        for j in range(len(board[0]))
        if board[i][j] == VISITED_CHAR
        and original_board[i][j] != GUARD_CHAR
        and does_create_loop(original_board, (i, j))
    )


VERIFICATION_COUNTER = 0


def does_create_loop(original_board: Board, pos: Position) -> bool:
    global VERIFICATION_COUNTER
    VERIFICATION_COUNTER += 1
    print(f"Counter: {VERIFICATION_COUNTER}")

    board = deep_copy_board(original_board)
    (i, j) = pos

    board[i][j] = OBSTACLE_CHAR

    return run_simulation(board)


def run_simulation(board: Board) -> bool:
    # Returns whether the guard looped
    # Modifies the board

    (i, j) = find_guard(board)
    direction = Direction.UP

    visited: Set[Tuple[Position, Direction]] = set()

    while is_valid_position((i, j), board):
        if ((i, j), direction) in visited:
            return True  # Loop

        visited.add(((i, j), direction))
        board[i][j] = VISITED_CHAR

        (next_i, next_j) = next_pos((i, j), direction)

        while (
            is_valid_position((next_i, next_j), board)
            and board[next_i][next_j] == OBSTACLE_CHAR
        ):
            direction = DIRECTION_ROTATION[direction]
            (next_i, next_j) = next_pos((i, j), direction)

        (i, j) = (next_i, next_j)

        # print_board(board)

    return False


def next_pos(pos: Position, direction: Direction) -> Position:
    (i, j) = pos
    (i_inc, j_inc) = DIRECTION_TO_POS_INC[direction]
    return (i + i_inc, j + j_inc)


def find_guard(board: Board) -> Position:
    return first(
        (i, j)
        for i in range(len(board))
        for j in range(len(board[0]))
        if board[i][j] == GUARD_CHAR
    )


def print_board(board: Board):
    s = "\n".join("".join(e for e in row) for row in board)
    print(s)
    print()


def is_valid_position(pos: Position, board: Board) -> bool:
    return (
        pos[0] >= 0
        and pos[0] < len(board)
        and pos[1] >= 0
        and pos[1] < len(board[pos[0]])
    )


def deep_copy_board(board: Board) -> Board:
    return [row.copy() for row in board]


def read_input(file_name: str) -> Board:
    with open(file_name) as f:
        return [[ch for ch in line.strip()] for line in f]


if __name__ == "__main__":
    main()
