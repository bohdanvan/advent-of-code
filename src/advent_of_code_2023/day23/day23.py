from collections import deque
import sys
from typing import Deque, Dict, List, Set, Tuple, TypedDict


PATH_TILE = "."
FOREST_TILE = "#"
SLOPE_UP_TILE = "^"
SLOPE_DOWN_TILE = "v"
SLOPE_RIGHT_TILE = ">"
SLOPE_LEFT_TILE = "<"

Board = List[List[str]]
Position = Tuple[int, int]

NEXT_POS_INC: Dict[str, List[Tuple[int, int]]] = {
    PATH_TILE: [(1, 0), (-1, 0), (0, 1), (0, -1)],
    FOREST_TILE: [],
    SLOPE_UP_TILE: [(-1, 0)],
    SLOPE_DOWN_TILE: [(1, 0)],
    SLOPE_RIGHT_TILE: [(0, 1)],
    SLOPE_LEFT_TILE: [(0, -1)],
}


class Candidate(TypedDict):
    pos: Position
    steps: int
    visited: Set[Position]


def main() -> None:
    input = read_input("src/advent_of_code_2023/day23/test.txt")
    board = parse_board(input)

    print(f"1 -> {solve_part1(board)}")
    print(f"2 -> {solve_part2(board)}")


def parse_board(lines: List[str]) -> Board:
    return [[ch for ch in line] for line in lines]


def solve_part1(board: Board) -> int:
    start = find_start(board)
    finish = find_finish(board)
    return find_longest_path(board, start, finish)


def solve_part2(board: Board) -> int:
    start = find_start(board)
    finish = find_finish(board)
    board = clear_slopes(board)
    return find_longest_path(board, start, finish)


def clear_slopes(board: Board) -> Board:
    return [
        [PATH_TILE if e != FOREST_TILE else FOREST_TILE for e in row] for row in board
    ]


def find_longest_path(board: Board, start: Position, finish: Position) -> int:
    sys.setrecursionlimit(10000)

    src_to_dest: Dict[Position, Tuple[Position, int, Position]] = dict()
    dest_to_src: Dict[Position, Position] = dict()

    def dfs(
        pos: Position,
        prev_pos: Position,
        steps: int,
        visited: Set[Position],
        max_steps: int,
    ) -> int:
        if pos == finish:
            print(f"Path found: {steps}")
            return max(max_steps, steps)

        visited.add(pos)

        if pos in src_to_dest:
            next_pos, step_inc, prev_to_next_pos = src_to_dest[pos]

            visited.add(prev_to_next_pos)

            res = dfs(next_pos, pos, steps + step_inc, visited, max_steps)

            visited.remove(prev_to_next_pos)
        else:
            step_inc = 1
            next_positions = [
                next_pos
                for next_pos in [
                    (pos[0] + i_inc, pos[1] + j_inc)
                    for i_inc, j_inc in NEXT_POS_INC[board[pos[0]][pos[1]]]
                ]
                if is_valid_position(next_pos, board)
                and board[next_pos[0]][next_pos[1]] != FOREST_TILE
                and next_pos not in visited
            ]

            if len(next_positions) == 1:
                next_pos = next_positions[0]

                if pos not in dest_to_src:
                    src_to_dest[pos] = (next_pos, 1, pos)
                    dest_to_src[next_pos] = pos
                else:
                    src = dest_to_src[pos]
                    _, step_inc, _ = src_to_dest[src]

                    src_to_dest[src] = (next_pos, step_inc + 1, pos)
                    dest_to_src[next_pos] = src

            res = max_steps
            if len(next_positions) > 0:
                res = max(
                    dfs(next_pos, pos, steps + step_inc, visited, max_steps)
                    for next_pos in next_positions
                )

        visited.remove(pos)

        return res

    # stack: Deque[Candidate] = deque()
    # stack.append(Candidate(pos=start, steps=0, visited=set()))

    # max_steps = 0

    # while len(stack) > 0:
    #     candidate = stack.pop()
    #     pos, steps, visited = candidate["pos"], candidate["steps"], candidate["visited"]

    return dfs(start, start, 0, set(), 0)


def find_start(board: Board) -> Position:
    return find_path_tile(board, 0)


def find_finish(board: Board) -> Position:
    return find_path_tile(board, len(board) - 1)


def find_path_tile(board: Board, i: int) -> Position:
    for j in range(len(board[i])):
        if board[i][j] == PATH_TILE:
            return (i, j)
    raise AssertionError("Path tile not found")


def is_valid_position(pos: Position, board: Board) -> bool:
    return (
        pos[0] >= 0
        and pos[0] < len(board)
        and pos[1] >= 0
        and pos[1] < len(board[pos[0]])
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
