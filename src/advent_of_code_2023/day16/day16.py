from collections import deque
from enum import Enum
from functools import reduce
from typing import Deque, Dict, List, Set, Tuple, TypedDict


class TileType(Enum):
    EMPTY = "."
    RIGHT_MIRROR = "/"
    LEFT_MIRROR = "\\"
    VERTICALL_SPLITTER = "|"
    HORIZONTAL_SPLITTER = "-"
    VISITED = "#"


Board = List[List[str]]
Position = Tuple[int, int]


class MoveType(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


Move = Tuple[Position, MoveType]


MOVE_TYPE_TO_POS_INC: Dict[MoveType, Tuple[int, int]] = {
    MoveType.LEFT: (0, -1),
    MoveType.RIGHT: (0, 1),
    MoveType.UP: (-1, 0),
    MoveType.DOWN: (1, 0),
}

MOVE_TRANSFORMATION: Dict[Tuple[TileType, MoveType], List[MoveType]] = {
    (TileType.EMPTY, MoveType.LEFT): [MoveType.LEFT],
    (TileType.EMPTY, MoveType.RIGHT): [MoveType.RIGHT],
    (TileType.EMPTY, MoveType.UP): [MoveType.UP],
    (TileType.EMPTY, MoveType.DOWN): [MoveType.DOWN],
    (TileType.RIGHT_MIRROR, MoveType.LEFT): [MoveType.DOWN],
    (TileType.RIGHT_MIRROR, MoveType.RIGHT): [MoveType.UP],
    (TileType.RIGHT_MIRROR, MoveType.UP): [MoveType.RIGHT],
    (TileType.RIGHT_MIRROR, MoveType.DOWN): [MoveType.LEFT],
    (TileType.LEFT_MIRROR, MoveType.LEFT): [MoveType.UP],
    (TileType.LEFT_MIRROR, MoveType.RIGHT): [MoveType.DOWN],
    (TileType.LEFT_MIRROR, MoveType.UP): [MoveType.LEFT],
    (TileType.LEFT_MIRROR, MoveType.DOWN): [MoveType.RIGHT],
    (TileType.VERTICALL_SPLITTER, MoveType.LEFT): [MoveType.UP, MoveType.DOWN],
    (TileType.VERTICALL_SPLITTER, MoveType.RIGHT): [MoveType.UP, MoveType.DOWN],
    (TileType.VERTICALL_SPLITTER, MoveType.UP): [MoveType.UP],
    (TileType.VERTICALL_SPLITTER, MoveType.DOWN): [MoveType.DOWN],
    (TileType.HORIZONTAL_SPLITTER, MoveType.LEFT): [MoveType.LEFT],
    (TileType.HORIZONTAL_SPLITTER, MoveType.RIGHT): [MoveType.RIGHT],
    (TileType.HORIZONTAL_SPLITTER, MoveType.UP): [MoveType.LEFT, MoveType.RIGHT],
    (TileType.HORIZONTAL_SPLITTER, MoveType.DOWN): [MoveType.LEFT, MoveType.RIGHT],
    (TileType.VISITED, MoveType.LEFT): [],
    (TileType.VISITED, MoveType.RIGHT): [],
    (TileType.VISITED, MoveType.UP): [],
    (TileType.VISITED, MoveType.DOWN): [],
}


def main() -> None:
    input = read_input("src/advent_of_code_2023/day16/input.txt")
    board = parse_board(input)

    print(f"1 -> {solve_part1(board)}")
    print(f"2 -> {solve_part2(board)}")


def solve_part1(board: Board) -> int:
    start_move = ((0, 0), MoveType.RIGHT)
    return count_energised_tiles(board, start_move)


def solve_part2(board: Board) -> int:
    start_moves = (
        [((i, 0), MoveType.RIGHT) for i in range(len(board))]
        + [((i, len(board[0]) - 1), MoveType.LEFT) for i in range(len(board))]
        + [((0, j), MoveType.DOWN) for j in range(len(board[0]))]
        + [((len(board) - 1, j), MoveType.DOWN) for j in range(len(board[0]))]
    )

    return max(count_energised_tiles(board, start_move) for start_move in start_moves)


def count_energised_tiles(board: Board, start_move: Move) -> int:
    move_queue: Deque[Move] = deque([start_move])
    visited_moves: Set[Move] = set()

    while len(move_queue) > 0:
        move = move_queue.popleft()
        pos, move_type = move
        visited_moves.add((pos, move_type))

        tile_type = TileType(board[pos[0]][pos[1]])

        next_move_types = MOVE_TRANSFORMATION[(tile_type, move_type)]
        for next_move_type in next_move_types:
            pos_inc = MOVE_TYPE_TO_POS_INC[next_move_type]
            next_pos = (pos[0] + pos_inc[0], pos[1] + pos_inc[1])
            new_move = (next_pos, next_move_type)
            if is_valid_position(next_pos, board) and new_move not in visited_moves:
                move_queue.append(new_move)

    # print_board(board, visited_moves)

    return len({pos for pos, move_type in visited_moves})


def is_valid_position(pos: Position, board: Board) -> bool:
    return (
        pos[0] >= 0
        and pos[0] < len(board)
        and pos[1] >= 0
        and pos[1] < len(board[pos[0]])
    )


def print_board(board: Board, visited_moves: Set[Move]):
    visited_pos = {pos for pos, move_type in visited_moves}
    s = "\n".join(
        "".join(
            board[i][j] if (i, j) not in visited_pos else "#"
            for j in range(len(board[0]))
        )
        for i in range(len(board))
    )
    print(s)


def parse_board(lines: List[str]) -> Board:
    return [[ch for ch in line] for line in lines]


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
