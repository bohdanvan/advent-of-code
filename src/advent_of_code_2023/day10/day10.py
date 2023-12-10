from itertools import count
from typing import Dict, List, Tuple, TypedDict, Optional, Set
from collections import deque
from enum import Enum


class Move(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Pipe(Enum):
    DOWN_UP = "|"
    LEFT_RIGHT = "-"
    UP_RIGHT = "L"
    UP_LEFT = "J"
    DOWN_LEFT = "7"
    DOWN_RIGHT = "F"
    GROUND = "."
    START = "S"


class AreaDirection(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class AreaPipe(Enum):
    OUTER = "O"
    INNER = "I"
    LOOP = "x"
    UNKNOWN = "-"


Position = Tuple[int, int]


class PathItem(TypedDict):
    pos: Position
    pipe: Pipe
    move: Move


AreaBoard = List[List[AreaPipe]]

NEXT_MOVE_MAPPING: Dict[Tuple[Pipe, Move], Move] = {
    (Pipe.DOWN_UP, Move.UP): Move.UP,
    (Pipe.DOWN_UP, Move.DOWN): Move.DOWN,
    (Pipe.LEFT_RIGHT, Move.RIGHT): Move.RIGHT,
    (Pipe.LEFT_RIGHT, Move.LEFT): Move.LEFT,
    (Pipe.UP_RIGHT, Move.DOWN): Move.RIGHT,
    (Pipe.UP_RIGHT, Move.LEFT): Move.UP,
    (Pipe.UP_LEFT, Move.DOWN): Move.LEFT,
    (Pipe.UP_LEFT, Move.RIGHT): Move.UP,
    (Pipe.DOWN_LEFT, Move.UP): Move.LEFT,
    (Pipe.DOWN_LEFT, Move.RIGHT): Move.DOWN,
    (Pipe.DOWN_RIGHT, Move.UP): Move.RIGHT,
    (Pipe.DOWN_RIGHT, Move.LEFT): Move.DOWN,
}

MOVE_POSITION_INC: Dict[Move, Tuple[int, int]] = {
    Move.UP: (-1, 0),
    Move.DOWN: (1, 0),
    Move.LEFT: (0, -1),
    Move.RIGHT: (0, 1),
}

FIRST_MOVE_MAPPING: Dict[Pipe, Move] = {
    Pipe.DOWN_UP: Move.UP,
    Pipe.LEFT_RIGHT: Move.RIGHT,
    Pipe.UP_RIGHT: Move.UP,
    Pipe.UP_LEFT: Move.UP,
    Pipe.DOWN_LEFT: Move.DOWN,
    Pipe.DOWN_RIGHT: Move.DOWN,
}

OUTER_MOVE_MAPPING: Dict[Tuple[Pipe, Move], List[Move]] = {
    (Pipe.DOWN_UP, Move.UP): [Move.LEFT],
    (Pipe.DOWN_UP, Move.DOWN): [Move.RIGHT],
    (Pipe.LEFT_RIGHT, Move.RIGHT): [Move.UP],
    (Pipe.LEFT_RIGHT, Move.LEFT): [Move.DOWN],
    (Pipe.UP_RIGHT, Move.DOWN): [],
    (Pipe.UP_RIGHT, Move.LEFT): [Move.DOWN, Move.LEFT],
    (Pipe.UP_LEFT, Move.DOWN): [Move.RIGHT, Move.DOWN],
    (Pipe.UP_LEFT, Move.RIGHT): [],
    (Pipe.DOWN_LEFT, Move.UP): [],
    (Pipe.DOWN_LEFT, Move.RIGHT): [Move.UP, Move.RIGHT],
    (Pipe.DOWN_RIGHT, Move.UP): [Move.LEFT, Move.UP],
    (Pipe.DOWN_RIGHT, Move.LEFT): [],
}


def main() -> None:
    board = read_input("src/advent_of_code_2023/day10/input.txt")

    print(f"1 -> {solve_part1(board)}")
    print(f"2 -> {solve_part2(board)}")


def solve_part1(board: List[str]) -> int:
    loop_path = find_loop_path(board)
    return len(loop_path) // 2


def traverse_loop(
    board: List[str], start: Position, start_pipe: Pipe
) -> Optional[List[PathItem]]:
    move = get_first_move(start_pipe)
    pos = get_next_position(start, move)

    path: List[PathItem] = [PathItem(pos=start, pipe=start_pipe, move=move)]

    while pos != start:
        if not is_valid_position(pos, board):
            return None

        pipe = Pipe(board[pos[0]][pos[1]])
        next_move = get_next_move(pipe, move)
        if next_move is None:
            return None
        move = next_move

        path.append(PathItem(pos=pos, pipe=pipe, move=move))
        pos = get_next_position(pos, move)

    if get_next_move(start_pipe, move) is None:
        return None

    return path


def find_loop_path(board: List[str]) -> List[PathItem]:
    start = find_start(board)
    start_pipes = [
        Pipe.DOWN_UP,
        Pipe.LEFT_RIGHT,
        Pipe.UP_RIGHT,
        Pipe.UP_LEFT,
        Pipe.DOWN_LEFT,
        Pipe.DOWN_RIGHT,
    ]

    loop_paths = [
        path
        for path in [
            traverse_loop(board, start, start_pipe) for start_pipe in start_pipes
        ]
        if path is not None
    ]
    if len(loop_paths) > 1:
        raise AssertionError(f"Multiple routes from {start}")
    if len(loop_paths) == 0:
        raise AssertionError(f"No routes from {start}")

    return loop_paths[0]


def is_valid_position(pos: Position, board: List[str]) -> bool:
    return (
        pos[0] >= 0
        and pos[0] < len(board)
        and pos[1] >= 0
        and pos[1] < len(board[pos[0]])
    )


def get_first_move(start_pipe: Pipe) -> Move:
    return FIRST_MOVE_MAPPING[start_pipe]


def get_next_position(pos: Position, move: Move) -> Position:
    pos_inc = MOVE_POSITION_INC[move]
    return (pos[0] + pos_inc[0], pos[1] + pos_inc[1])


def get_next_move(pipe: Pipe, prev_move: Move) -> Optional[Move]:
    return NEXT_MOVE_MAPPING.get((pipe, prev_move), None)


def find_start(board: List[str]) -> Position:
    for i in range(len(board)):
        for j in range(len(board[i])):
            if Pipe(board[i][j]) == Pipe.START:
                return (i, j)
    raise AssertionError("Start not found")


def solve_part2(board: List[str]) -> int:
    loop_path = find_loop_path(board)

    border_path_idx = min(
        [idx for idx, path_item in enumerate(loop_path) if path_item["pos"][0] == 0],
        key=lambda idx: loop_path[idx]["pos"][1],
    )
    loop_path = (
        loop_path[border_path_idx:] + loop_path[0:border_path_idx]
    )  # start from border path

    area_board = build_area_board(board, loop_path)
    fill_outer_border(board, loop_path, area_board)

    fill_all_outer_area(board, area_board)
    print_area_board(area_board)

    return sum(
        1
        for i in range(len(area_board))
        for j in range(len(area_board[i]))
        if area_board[i][j] == AreaPipe.UNKNOWN
    )


def fill_all_outer_area(board: List[str], area_board: AreaBoard):
    outer_pos_queue = deque(
        (i, j)
        for i in range(len(area_board))
        for j in range(len(area_board[i]))
        if area_board[i][j] == AreaPipe.OUTER
    )

    while len(outer_pos_queue) > 0:
        pos = outer_pos_queue.pop()

        next_positions = [
            get_next_position(pos, Move.UP),
            get_next_position(pos, Move.DOWN),
            get_next_position(pos, Move.LEFT),
            get_next_position(pos, Move.RIGHT),
        ]

        for next_pos in next_positions:
            if (
                is_valid_position(next_pos, board)
                and area_board[next_pos[0]][next_pos[1]] == AreaPipe.UNKNOWN
            ):
                area_board[next_pos[0]][next_pos[1]] = AreaPipe.OUTER
                outer_pos_queue.append(next_pos)


def fill_outer_border(
    board: List[str], loop_path: List[PathItem], area_board: AreaBoard
):
    for idx, path_item in enumerate(loop_path):
        pos, pipe, move = path_item["pos"], path_item["pipe"], path_item["move"]
        outer_moves = OUTER_MOVE_MAPPING[(pipe, loop_path[idx - 1]["move"])]
        for outer_move in outer_moves:
            outer_pos = get_next_position(pos, outer_move)
            if (
                is_valid_position(outer_pos, board)
                and area_board[outer_pos[0]][outer_pos[1]] == AreaPipe.UNKNOWN
            ):
                area_board[outer_pos[0]][outer_pos[1]] = AreaPipe.OUTER


def build_area_board(board: List[str], loop_path: List[PathItem]) -> AreaBoard:
    area_board = [[AreaPipe.UNKNOWN for pipe in row] for row in board]
    for path_item in loop_path:
        i, j = path_item["pos"]
        area_board[i][j] = AreaPipe.LOOP
    return area_board


def print_area_board(area_board: AreaBoard):
    s = "\n".join("".join(pipe.value for pipe in row) for row in area_board)
    print(s)


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
