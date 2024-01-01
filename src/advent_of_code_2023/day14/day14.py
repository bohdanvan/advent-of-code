from typing import Dict, List, Optional, Tuple, TypeVar, TypedDict

ROUNDED_ROCK = "O"
CUBE_ROCK = "#"
EMPTY_SPACE = "."


class Cycle(TypedDict):
    offset: int
    len: int


def main() -> None:
    input = read_input("src/advent_of_code_2023/day14/input.txt")
    board = parse(input)

    print(f"1 -> {solve_part1(board)}")
    print(f"2 -> {solve_part2(board, 1000000000)}")


def solve_part1(board: List[List[str]]) -> int:
    board = tilt_north(board)
    return calc_total_load(board)


def solve_part2(board: List[List[str]], spin_iteration: int) -> int:
    board = find_board(board, spin_iteration)
    return calc_total_load(board)


def find_board(board: List[List[str]], spin_iteration: int) -> List[List[str]]:
    board_to_id: Dict[str, int] = {matrix_to_string(board): 0}
    id_to_board: Dict[int, List[List[str]]] = {0: board}

    for id in range(1, 1001):
        print(f"id = {id}")
        board = spin_cycle(board)

        key = matrix_to_string(board)
        if key in board_to_id:
            offset = board_to_id[key]
            cycle_len = id - offset

            iterations = offset + (spin_iteration - offset) % cycle_len
            print(f"iterations = {iterations}")
            return id_to_board[iterations]

        board_to_id[key] = id
        id_to_board[id] = [row.copy() for row in board]

    raise AssertionError("Not found")


def calc_total_load(board: List[List[str]]) -> int:
    return sum(
        len(board) - i
        for j in range(len(board[0]))
        for i in range(len(board))
        if board[i][j] == ROUNDED_ROCK
    )


def spin_cycle(board: List[List[str]]) -> List[List[str]]:
    board = tilt_north(board)
    board = tilt_west(board)
    board = tilt_south(board)
    board = tilt_east(board)
    return board


def tilt_north(board: List[List[str]]) -> List[List[str]]:
    for j in range(len(board[0])):
        empty_idx = 0

        for i in range(len(board)):
            if board[i][j] == CUBE_ROCK:
                empty_idx = i + 1
            elif board[i][j] == ROUNDED_ROCK:
                board[i][j] = EMPTY_SPACE
                board[empty_idx][j] = ROUNDED_ROCK
                empty_idx += 1

    return board


def tilt_west(board: List[List[str]]) -> List[List[str]]:
    board = rotate270(board)
    tilt_north(board)
    return rotate90(board)


def tilt_south(board: List[List[str]]) -> List[List[str]]:
    board = rotate180(board)
    tilt_north(board)
    return rotate180(board)


def tilt_east(board: List[List[str]]) -> List[List[str]]:
    board = rotate90(board)
    tilt_north(board)
    return rotate270(board)


def parse(lines: List[str]) -> List[List[str]]:
    return [list(line) for line in lines]


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


# Matrix Functions

T = TypeVar("T")


def rotate90(matrix: List[List[T]]) -> List[List[T]]:
    return [
        [matrix[i][j] for i in range(len(matrix))]
        for j in reversed(range(len(matrix[0])))
    ]


def rotate180(matrix: List[List[T]]) -> List[List[T]]:
    return rotate90(rotate90(matrix))


def rotate270(matrix: List[List[T]]) -> List[List[T]]:
    return rotate90(rotate90(rotate90(matrix)))


def print_matrix(
    matrix: List[List[T]], delimiter: str = "", desc: Optional[str] = None
):
    print(f"-----------{' '+desc+ ' ' if desc is not None else ''}-----------")
    print(matrix_to_string(matrix, delimiter))


def matrix_to_string(matrix: List[List[T]], delimiter: str = "") -> str:
    return "\n".join(delimiter.join(str(e) for e in row) for row in matrix)


if __name__ == "__main__":
    main()
