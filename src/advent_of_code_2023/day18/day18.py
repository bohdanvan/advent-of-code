from collections import deque
from enum import Enum
from typing import Deque, Dict, List, Tuple, TypedDict

from more_itertools import first


class MoveType(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


CODE_TO_MOVE_TYPE: Dict[int, MoveType] = {
    0: MoveType.RIGHT,
    1: MoveType.DOWN,
    2: MoveType.LEFT,
    3: MoveType.UP,
}


class Move(TypedDict):
    type: MoveType
    steps: int


class BoardStats(TypedDict):
    min_row: int
    max_row: int
    min_col: int
    max_col: int


GROUND_TILE = "."
TRENCH_TILE = "#"

Board = List[List[str]]
Position = Tuple[int, int]


class ScaledBoard(TypedDict):
    board: Board
    row_scales: List[int]
    col_scales: List[int]


MOVE_TYPE_TO_POS_INC: Dict[MoveType, Tuple[int, int]] = {
    MoveType.LEFT: (0, -1),
    MoveType.RIGHT: (0, 1),
    MoveType.UP: (-1, 0),
    MoveType.DOWN: (1, 0),
}

POS_INC: List[Tuple[int, int]] = [(0, -1), (0, 1), (-1, 0), (1, 0)]

INF_INT = 1000000000000000


def main() -> None:
    input = read_input("src/advent_of_code_2023/day18/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


### PART 1 ###


def solve_part1(lines: List[str]) -> int:
    moves = parse_moves(lines)
    board_stats = find_board_stats(moves)
    rows = board_stats["max_row"] - board_stats["min_row"] + 1
    cols = board_stats["max_col"] - board_stats["min_col"] + 1

    board = create_board(rows, cols)
    start_pos = (-board_stats["min_row"], -board_stats["min_col"])
    apply_moves(board, moves, start_pos)
    # print_board(board)

    fill_inside(board)

    return count_tiles(board, TRENCH_TILE)


def create_board(rows: int, cols: int) -> Board:
    return [[GROUND_TILE for j in range(cols)] for i in range(rows)]


def print_board(board: Board):
    s = "\n".join("".join(e for e in row) for row in board)
    print(s)


def count_tiles(board: Board, tile: str) -> int:
    return sum(sum(1 if t == tile else 0 for t in row) for row in board)


def find_board_stats(moves: List[Move]) -> BoardStats:
    board_stats = BoardStats(min_row=0, max_row=0, min_col=0, max_col=0)

    pos = (0, 0)
    for move in moves:
        pos_inc = MOVE_TYPE_TO_POS_INC[move["type"]]
        pos = (pos[0] + pos_inc[0] * move["steps"], pos[1] + pos_inc[1] * move["steps"])
        board_stats = BoardStats(
            min_row=min(board_stats["min_row"], pos[0]),
            max_row=max(board_stats["max_row"], pos[0]),
            min_col=min(board_stats["min_col"], pos[1]),
            max_col=max(board_stats["max_col"], pos[1]),
        )

    return board_stats


def apply_moves(board: Board, moves: List[Move], start_pos: Position):
    pos = start_pos
    board[pos[0]][pos[1]] = TRENCH_TILE

    for move in moves:
        pos_inc = MOVE_TYPE_TO_POS_INC[move["type"]]
        for _ in range(move["steps"]):
            pos = (pos[0] + pos_inc[0], pos[1] + pos_inc[1])
            board[pos[0]][pos[1]] = TRENCH_TILE


def fill_inside(board: Board, start_row: int = 0):
    start_pos = find_pos_inside(board, start_row)
    pos_queue: Deque[Position] = deque([start_pos])

    while len(pos_queue) > 0:
        pos = pos_queue.pop()
        board[pos[0]][pos[1]] = TRENCH_TILE

        for pos_inc in POS_INC:
            new_pos = (pos[0] + pos_inc[0], pos[1] + pos_inc[1])
            if board[new_pos[0]][new_pos[1]] == GROUND_TILE:
                pos_queue.append(new_pos)


def find_pos_inside(board: Board, start_row: int) -> Position:
    first_trench_col = first(
        j for j in range(len(board[0])) if board[start_row][j] == TRENCH_TILE
    )
    return (start_row + 1, first_trench_col + 1)


def parse_moves(lines: List[str]) -> List[Move]:
    return [parse_move(line) for line in lines]


def parse_move(s: str) -> Move:
    parts = s.split()
    return Move(type=MoveType(parts[0]), steps=int(parts[1]))


### PART 2 ###


def solve_part2(lines: List[str]) -> int:
    moves = parse_moves_part2(lines)
    scaled_board = apply_moves_part2(moves)
    # print_scaled_board(scaled_board)
    fill_inside(scaled_board["board"], 1)
    # print_scaled_board(scaled_board)
    return count_scaled_tiles(scaled_board, TRENCH_TILE)


def apply_moves_part2(moves: List[Move]) -> ScaledBoard:
    scaled_board = ScaledBoard(
        board=[[GROUND_TILE] * 3 for _ in range(3)],
        row_scales=[INF_INT, 1, INF_INT],
        col_scales=[INF_INT, 1, INF_INT],
    )
    board, row_scales, col_scales = (
        scaled_board["board"],
        scaled_board["row_scales"],
        scaled_board["col_scales"],
    )

    row, col = 1, 1
    for move in moves:
        steps = move["steps"]

        if move["type"] == MoveType.RIGHT:
            col += 1
            while steps > 0 and col_scales[col] <= steps:
                board[row][col] = TRENCH_TILE
                steps -= col_scales[col]
                col += 1

            if steps == 0:
                col -= 1
            elif steps > 1:
                split_col(scaled_board, col, [steps - 1, 1, col_scales[col] - steps])
                board[row][col] = TRENCH_TILE
                col += 1
                board[row][col] = TRENCH_TILE
            elif steps == 1:
                split_col(scaled_board, col, [1, col_scales[col] - 1])
                board[row][col] = TRENCH_TILE
        elif move["type"] == MoveType.LEFT:
            col -= 1
            while steps > 0 and col_scales[col] <= steps:
                board[row][col] = TRENCH_TILE
                steps -= col_scales[col]
                col -= 1

            if steps == 0:
                col += 1
            elif steps > 1:
                split_col(scaled_board, col, [col_scales[col] - steps, 1, steps - 1])
                col += 2
                board[row][col] = TRENCH_TILE
                col -= 1
                board[row][col] = TRENCH_TILE
            elif steps == 1:
                split_col(scaled_board, col, [col_scales[col] - 1, 1])
                col += 1
                board[row][col] = TRENCH_TILE
        elif move["type"] == MoveType.DOWN:
            row += 1
            while steps > 0 and row_scales[row] <= steps:
                board[row][col] = TRENCH_TILE
                steps -= row_scales[row]
                row += 1

            if steps == 0:
                row -= 1
            elif steps > 1:
                split_row(scaled_board, row, [steps - 1, 1, row_scales[row] - steps])
                board[row][col] = TRENCH_TILE
                row += 1
                board[row][col] = TRENCH_TILE
            elif steps == 1:
                split_col(scaled_board, row, [1, row_scales[row] - 1])
                board[row][col] = TRENCH_TILE
        elif move["type"] == MoveType.UP:
            row -= 1
            while steps > 0 and row_scales[row] <= steps:
                board[row][col] = TRENCH_TILE
                steps -= row_scales[row]
                row -= 1

            if steps == 0:
                row += 1
            elif steps > 1:
                split_row(scaled_board, row, [row_scales[row] - steps, 1, steps - 1])
                row += 2
                board[row][col] = TRENCH_TILE
                row -= 1
                board[row][col] = TRENCH_TILE
            elif steps == 1:
                split_row(scaled_board, row, [row_scales[row] - 1, 1])
                row += 1
                board[row][col] = TRENCH_TILE

    return scaled_board


def split_col(scaled_board: ScaledBoard, col: int, col_scales: List[int]):
    scaled_board["col_scales"][col] = col_scales[0]
    col += 1

    for col_scale in col_scales[1:]:
        for row in scaled_board["board"]:
            row.insert(col, row[col - 1])
        scaled_board["col_scales"].insert(col, col_scale)
        col += 1


def split_row(scaled_board: ScaledBoard, row: int, row_scales: List[int]):
    scaled_board["row_scales"][row] = row_scales[0]
    row += 1

    for row_scale in row_scales[1:]:
        scaled_board["board"].insert(
            row,
            [
                scaled_board["board"][row - 1][j]
                for j in range(len(scaled_board["board"][0]))
            ],
        )
        scaled_board["row_scales"].insert(row, row_scale)
        row += 1


def count_scaled_tiles(scaled_board: ScaledBoard, tile: str) -> int:
    board, row_scales, col_scales = (
        scaled_board["board"],
        scaled_board["row_scales"],
        scaled_board["col_scales"],
    )
    return sum(
        sum(
            row_scales[i] * col_scales[j] if board[i][j] == tile else 0
            for j in range(len(board[0]))
        )
        for i in range(len(board))
    )


def print_scaled_board(scaled_board: ScaledBoard):
    print(f"row_scales = {scaled_board['row_scales']}")
    print(f"col_scales = {scaled_board['col_scales']}")
    print_board(scaled_board["board"])


def parse_moves_part2(lines: List[str]) -> List[Move]:
    return [parse_move_part2(line) for line in lines]


def parse_move_part2(s: str) -> Move:
    parts = s.split()
    return Move(type=CODE_TO_MOVE_TYPE[int(parts[2][7])], steps=int(parts[2][2:7], 16))


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
