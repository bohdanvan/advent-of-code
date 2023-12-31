from enum import Enum
from operator import itemgetter
from queue import PriorityQueue
import re
from typing import Dict, List, Set, Tuple


class MoveType(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


MOVE_TYPE_TO_POS_INC: Dict[MoveType, Tuple[int, int]] = {
    MoveType.LEFT: (0, -1),
    MoveType.RIGHT: (0, 1),
    MoveType.UP: (-1, 0),
    MoveType.DOWN: (1, 0),
}

INVERTED_MOVE_TYPE: Dict[MoveType, MoveType] = {
    MoveType.LEFT: MoveType.RIGHT,
    MoveType.RIGHT: MoveType.LEFT,
    MoveType.UP: MoveType.DOWN,
    MoveType.DOWN: MoveType.UP,
}

MOVE_TURN: Dict[MoveType, Set[MoveType]] = {
    MoveType.LEFT: {MoveType.UP, MoveType.DOWN},
    MoveType.RIGHT: {MoveType.UP, MoveType.DOWN},
    MoveType.UP: {MoveType.LEFT, MoveType.RIGHT},
    MoveType.DOWN: {MoveType.LEFT, MoveType.RIGHT},
}

Board = List[List[int]]
Position = Tuple[int, int]
Move = Tuple[Position, MoveType, int]

MAX_STEPS = 10  # 3
MIN_STEPS = 4
MAX_LOSS = 1000000000000


class _PriorityQueueWrapper:
    def __init__(self, item, key):
        self.item = item
        self.key = key

    def __lt__(self, other):
        return self.key(self.item) < other.key(other.item)

    def __eq__(self, other):
        return self.key(self.item) == other.key(other.item)


class KeyPriorityQueue(PriorityQueue):
    def __init__(self, key):
        self.key = key
        super().__init__()

    def _qsize(self):
        return super()._qsize()

    def _get(self):
        wrapper = super()._get()
        return wrapper.item

    def _put(self, item):
        super()._put(_PriorityQueueWrapper(item, self.key))


def main() -> None:
    input = read_input("src/advent_of_code_2023/day17/test.txt")
    board = parse_board(input)

    print(f"1 -> {solve(board, min_steps=1, max_steps=3)}")
    print(f"2 -> {solve(board, min_steps=4, max_steps=10)}")


def solve(board: Board, min_steps: int = MIN_STEPS, max_steps: int = MAX_STEPS) -> int:
    move_loss: Dict[Move, int] = dict()
    move_pq: PriorityQueue[Tuple[Move, int]] = KeyPriorityQueue(itemgetter(1))
    move_pq.put(
        (
            ((0, min_steps), MoveType.RIGHT, min_steps),
            sum(board[0][j] for j in range(1, min_steps + 1)),
        )
    )
    move_pq.put(
        (
            ((min_steps, 0), MoveType.DOWN, min_steps),
            sum(board[i][0] for i in range(1, min_steps + 1)),
        )
    )

    while not move_pq.empty():
        move, loss = move_pq.get()
        pos, move_type, steps = move

        if loss >= move_loss.get(move, MAX_LOSS):
            continue

        move_loss[move] = loss

        for next_move_type in find_next_moves(move_type, steps, min_steps, max_steps):
            pos_inc = MOVE_TYPE_TO_POS_INC[next_move_type]

            if next_move_type == move_type:
                next_pos = (pos[0] + pos_inc[0], pos[1] + pos_inc[1])
                next_steps = steps + 1
            else:
                next_pos = (
                    pos[0] + min_steps * pos_inc[0],
                    pos[1] + min_steps * pos_inc[1],
                )
                next_steps = min_steps

            next_move = (next_pos, next_move_type, next_steps)

            if is_valid_position(next_pos, board):
                next_loss = (
                    loss
                    + sum(
                        board[i][j]
                        for i in range(
                            min(pos[0], next_pos[0]), max(pos[0], next_pos[0]) + 1
                        )
                        for j in range(
                            min(pos[1], next_pos[1]), max(pos[1], next_pos[1]) + 1
                        )
                    )
                    - board[pos[0]][pos[1]]
                )
                move_pq.put((next_move, next_loss))

    # print_move_loss(move_loss, board)
    # print("----------")

    return min(
        loss
        for (pos, _, _), loss in move_loss.items()
        if pos == (len(board) - 1, len(board[0]) - 1)
    )


def find_next_moves(
    move_type: MoveType, steps: int, min_steps: int, max_steps: int
) -> Set[MoveType]:
    if steps < min_steps:
        return {move_type}
    elif steps == max_steps:
        return MOVE_TURN[move_type]
    else:
        return {mt for mt in MoveType if mt != INVERTED_MOVE_TYPE[move_type]}


def print_move_loss(move_loss: Dict[Move, int], board: Board):
    grouped_by_pos: Dict[Position, List[Tuple[Move, int]]] = {}
    for move, loss in move_loss.items():
        if move[0] not in grouped_by_pos:
            grouped_by_pos[move[0]] = []
        grouped_by_pos[move[0]].append((move, loss))

    s = "\n".join(
        "\t".join(
            format_moves(grouped_by_pos.get((i, j), list()))
            if (i, j) in grouped_by_pos
            else "-"
            for j in range(len(board[0]))
        )
        for i in range(len(board))
    )
    print(s)


def format_moves(moves: List[Tuple[Move, int]]) -> str:
    return (
        "["
        + ",".join(
            f"{move_type.value}:{steps}|{loss}"
            for ((pos, move_type, steps), loss) in moves
        )
        + "]"
    )


def is_valid_position(pos: Position, board: List[List[int]]) -> bool:
    return (
        pos[0] >= 0
        and pos[0] < len(board)
        and pos[1] >= 0
        and pos[1] < len(board[pos[0]])
    )


def parse_board(lines: List[str]) -> Board:
    return [[int(ch) for ch in line] for line in lines]


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
