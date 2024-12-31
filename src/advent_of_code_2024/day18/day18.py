from bisect import bisect_right
from queue import PriorityQueue
from typing import Callable, List, Optional, Set, Tuple

from matplotlib.pylab import f

from utils.utils import bisect_left_lambda

TEST_BOARD_SIZE = (7, 7)
BOARD_SIZE = (71, 71)

TEST_BLOCKS_COUNT = 12
BLOCKS_COUNT = 1024

Board = List[List[str]]
Pos = Tuple[int, int]

POS_INCS: List[Tuple[int, int]] = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


def main() -> None:
    input = read_input("src/advent_of_code_2024/day18/input.txt")

    # print(f"1 -> {solve_part1(input, TEST_BOARD_SIZE, TEST_BLOCKS_COUNT)}")
    # print(f"2 -> {solve_part2(input, TEST_BOARD_SIZE)}")

    print(f"1 -> {solve_part1(input, BOARD_SIZE, BLOCKS_COUNT)}")
    print(f"2 -> {solve_part2(input, BOARD_SIZE)}")


def solve_part1(
    input: List[str], board_size: Tuple[int, int], blocks_count: int
) -> int:
    block_cells = parse(input)
    board = create_board(board_size, set(block_cells[:blocks_count]))
    res = find_shortest_path(board)
    if res is None:
        raise Exception("No path found")
    return res


def solve_part2(input: List[str], board_size: Tuple[int, int]) -> str:
    block_cells = parse(input)

    unreachable_blocks_count = bisect_left_lambda(
        block_cells,
        verifier=lambda blocks_count: is_reachable(
            board_size, block_cells, blocks_count
        ),
    )
    path_blocking_cell = block_cells[unreachable_blocks_count - 1]

    return ",".join(map(str, [path_blocking_cell[1], path_blocking_cell[0]]))


def is_reachable(
    board_size: Tuple[int, int], block_cells: List[Pos], blocks_count: int
) -> bool:
    board = create_board(board_size, set(block_cells[:blocks_count]))
    res = find_shortest_path(board)
    return res is not None


def find_shortest_path(board: Board) -> Optional[int]:
    start_pos = (0, 0)
    end_pos = (len(board) - 1, len(board[0]) - 1)

    visited: Set[Pos] = set()

    moves_pq: PriorityQueue[Tuple[int, Pos]] = PriorityQueue()
    moves_pq.put((0, start_pos))

    while not moves_pq.empty():
        steps, (i, j) = moves_pq.get()

        if (i, j) == end_pos:
            return steps

        if (i, j) in visited:
            continue

        visited.add((i, j))

        for i_inc, j_inc in POS_INCS:
            next_i, next_j = i + i_inc, j + j_inc
            if (
                is_valid_position((next_i, next_j), board)
                and board[next_i][next_j] == "."
            ):
                moves_pq.put((steps + 1, (next_i, next_j)))

    return None


def create_board(board_size: Tuple[int, int], block_cells: Set[Pos]) -> Board:
    return [
        ["#" if (i, j) in block_cells else "." for j in range(board_size[1])]
        for i in range(board_size[0])
    ]


def print_board(board: Board):
    s = "\n".join("".join(e for e in row) for row in board)
    print(s)


def is_valid_position(pos: Pos, board: List[List[str]]) -> bool:
    i, j = pos
    return i >= 0 and i < len(board) and j >= 0 and j < len(board[i])


def parse(input: List[str]) -> List[Pos]:
    return list(map(parse_pos, input))


def parse_pos(line: str) -> Pos:
    parsed_line = list(map(int, line.split(",")))
    return (parsed_line[1], parsed_line[0])


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
