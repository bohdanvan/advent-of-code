from collections import deque
from dataclasses import dataclass
from enum import StrEnum
import time
from typing import Collection, Deque, Dict, List, Tuple

from more_itertools import first, flatten


Board = List[List[str]]
Pos = Tuple[int, int]


@dataclass
class Move:
    old_pos: Pos
    new_pos: Pos

    def to_tuple(self) -> Tuple[Pos, Pos]:
        return (self.old_pos, self.new_pos)


class MoveType(StrEnum):
    LEFT = "<"
    RIGHT = ">"
    UP = "^"
    DOWN = "v"


MOVE_TYPE_TO_POS_INC: Dict[MoveType, Tuple[int, int]] = {
    MoveType.LEFT: (0, -1),
    MoveType.RIGHT: (0, 1),
    MoveType.UP: (-1, 0),
    MoveType.DOWN: (1, 0),
}


ROBOT_CELL = "@"
BOX_CELL = "O"
WALL_CELL = "#"
EMPTY_CELL = "."
LARGE_BOX_LEFT_CELL = "["
LARGE_BOX_RIGHT_CELL = "]"

LARGE_BOX_CELLS = {LARGE_BOX_LEFT_CELL, LARGE_BOX_RIGHT_CELL}
BLOCKED_CELLS = {WALL_CELL, ROBOT_CELL}


def main() -> None:
    input = read_input("src/advent_of_code_2024/day15/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(input: List[str]) -> int:
    board, move_types = parse(input)
    run_all_moves(move_types, board)
    return board_score(board)


def solve_part2(input: List[str]) -> int:
    board, move_types = parse(input)
    board = build_extended_board(board)
    run_all_moves(move_types, board)
    return board_score(board)


def run_all_moves(move_types: List[MoveType], board: Board):
    pos = find_robot_pos(board)
    print_board(board)

    idx = 0
    for move_type in move_types:
        pos = move_robot(pos, move_type, board)
        # if idx % 30 == 0:
        #     print_board(board)
        #     time.sleep(0.01)
        # idx += 1


def move_robot(robot_pos: Pos, move_type: MoveType, board: Board) -> Pos:
    i, j = robot_pos
    next_i, next_j = next_move_pos(robot_pos, move_type)

    if board[next_i][next_j] == BOX_CELL:
        move_box((next_i, next_j), move_type, board)

    if board[next_i][next_j] in (LARGE_BOX_LEFT_CELL, LARGE_BOX_RIGHT_CELL):
        move_large_box((next_i, next_j), move_type, board)

    if board[next_i][next_j] == EMPTY_CELL:
        board[i][j] = EMPTY_CELL
        board[next_i][next_j] = ROBOT_CELL
        return (next_i, next_j)

    return robot_pos


def move_box(pos: Pos, move_type: MoveType, board: Board):
    i, j = pos
    if board[i][j] != BOX_CELL:
        return

    next_i, next_j = next_move_pos(pos, move_type)
    if board[next_i][next_j] == BOX_CELL:
        move_box((next_i, next_j), move_type, board)

    if board[next_i][next_j] == EMPTY_CELL:
        board[i][j] = EMPTY_CELL
        board[next_i][next_j] = BOX_CELL


def move_large_box(pos: Pos, move_type: MoveType, board: Board):
    moves_queue: Deque[Move] = deque()
    simulate_large_box_move(pos, move_type, board, moves_queue)

    for move in moves_queue:
        (i, j), (new_i, new_j) = move.to_tuple()

        assert board[i][j] in (
            LARGE_BOX_LEFT_CELL,
            LARGE_BOX_RIGHT_CELL,
        ), f"Can't move non-box cell '{board[i][j]}': ({i}, {j})"
        assert (
            board[new_i][new_j] == EMPTY_CELL
        ), f"Can't move to not empty cell 'board[new_i][new_j]': ({i}, {j})"

        board[new_i][new_j] = board[i][j]
        board[i][j] = EMPTY_CELL


def simulate_large_box_move(
    pos: Pos, move_type: MoveType, board: Board, moves_queue: Deque[Move]
):
    i, j = pos
    if board[i][j] == EMPTY_CELL:
        return
    if board[i][j] not in (LARGE_BOX_LEFT_CELL, LARGE_BOX_RIGHT_CELL):
        return
    if board[i][j] == LARGE_BOX_RIGHT_CELL:
        simulate_large_box_move((i, j - 1), move_type, board, moves_queue)
        return

    next_pos_left = next_move_pos((i, j), move_type)
    next_pos_right = next_move_pos((i, j + 1), move_type)
    if move_type == MoveType.LEFT:
        if board[next_pos_left[0]][next_pos_left[1]] in BLOCKED_CELLS:
            moves_queue.clear()
            return

        if board[next_pos_left[0]][next_pos_left[1]] in LARGE_BOX_CELLS:
            simulate_large_box_move(next_pos_left, move_type, board, moves_queue)
            if not moves_queue:
                return

        append_if_not_exist(
            moves_queue,
            Move(
                old_pos=(i, j),
                new_pos=next_pos_left,
            ),
        )
        append_if_not_exist(
            moves_queue,
            Move(
                old_pos=(i, j + 1),
                new_pos=next_pos_right,
            ),
        )
    elif move_type == MoveType.RIGHT:
        if board[next_pos_right[0]][next_pos_right[1]] in BLOCKED_CELLS:
            moves_queue.clear()
            return

        if board[next_pos_right[0]][next_pos_right[1]] in LARGE_BOX_CELLS:
            simulate_large_box_move(next_pos_right, move_type, board, moves_queue)
            if not moves_queue:
                return

        append_if_not_exist(
            moves_queue,
            Move(
                old_pos=(i, j + 1),
                new_pos=next_pos_right,
            ),
        )
        append_if_not_exist(
            moves_queue,
            Move(
                old_pos=(i, j),
                new_pos=next_pos_left,
            ),
        )
    elif move_type in (MoveType.UP, MoveType.DOWN):
        if (
            board[next_pos_left[0]][next_pos_left[1]] in BLOCKED_CELLS
            or board[next_pos_right[0]][next_pos_right[1]] in BLOCKED_CELLS
        ):
            moves_queue.clear()
            return

        if board[next_pos_left[0]][next_pos_left[1]] in LARGE_BOX_CELLS:
            left_move_stack: Deque[Move] = deque()
            simulate_large_box_move(next_pos_left, move_type, board, left_move_stack)
            if not left_move_stack:
                moves_queue.clear()
                return
            extend_if_not_exist(moves_queue, left_move_stack)

        if board[next_pos_right[0]][next_pos_right[1]] == LARGE_BOX_LEFT_CELL:
            right_move_stack: Deque[Move] = deque()
            simulate_large_box_move(next_pos_right, move_type, board, right_move_stack)
            if not right_move_stack:
                moves_queue.clear()
                return
            extend_if_not_exist(moves_queue, right_move_stack)

        append_if_not_exist(
            moves_queue,
            Move(
                old_pos=(i, j),
                new_pos=next_pos_left,
            ),
        )
        append_if_not_exist(
            moves_queue,
            Move(
                old_pos=(i, j + 1),
                new_pos=next_pos_right,
            ),
        )


def append_if_not_exist(queue: Deque[Move], move: Move):
    if move not in queue:
        queue.append(move)


def extend_if_not_exist(queue: Deque[Move], moves: Collection[Move]):
    for move in moves:
        append_if_not_exist(queue, move)


def next_move_pos(pos: Pos, move_type: MoveType) -> Pos:
    pos_inc = MOVE_TYPE_TO_POS_INC[move_type]
    return (pos[0] + pos_inc[0], pos[1] + pos_inc[1])


def find_robot_pos(board: Board) -> Pos:
    return first(
        (i, j)
        for i in range(len(board))
        for j in range(len(board[0]))
        if board[i][j] == ROBOT_CELL
    )


def board_score(board: Board) -> int:
    return sum(
        100 * i + j
        for i in range(len(board))
        for j in range(len(board[0]))
        if board[i][j] in (BOX_CELL, LARGE_BOX_LEFT_CELL)
    )


def build_extended_board(board: Board) -> Board:
    return [list(flatten([build_extended_cell(cell) for cell in row])) for row in board]


def build_extended_cell(cell: str) -> List[str]:
    if cell == WALL_CELL:
        return [WALL_CELL, WALL_CELL]
    elif cell == BOX_CELL:
        return [LARGE_BOX_LEFT_CELL, LARGE_BOX_RIGHT_CELL]
    elif cell == ROBOT_CELL:
        return [ROBOT_CELL, EMPTY_CELL]
    else:
        return [EMPTY_CELL, EMPTY_CELL]


def copy_board(board: Board) -> Board:
    return [row.copy() for row in board]


def print_board(board: Board):
    print("\n".join("".join(e for e in row) for row in board))
    print()


def parse(input: List[str]) -> Tuple[Board, List[MoveType]]:
    break_idx = input.index("")

    return (
        [[ch for ch in row] for row in input[0:break_idx]],
        [MoveType(ch) for ch in "".join(input[break_idx:])],
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
