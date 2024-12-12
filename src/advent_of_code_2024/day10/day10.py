from curses.ascii import isdigit
from typing import List, Set, Tuple

Board = List[List[int]]
Pos = Tuple[int, int]


def main() -> None:
    input = read_input("src/advent_of_code_2024/day10/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(input: List[str]) -> int:
    board = parse_board(input)
    trail_starts = find_trail_starts(board)

    return sum(
        traverse_path_with_score(trail_start, board, set())
        for trail_start in trail_starts
    )


def solve_part2(input: List[str]) -> int:
    board = parse_board(input)
    trail_starts = find_trail_starts(board)

    return sum(
        traverse_path_with_rating(trail_start, board) for trail_start in trail_starts
    )


def find_trail_starts(board: Board) -> List[Pos]:
    return [
        (i, j)
        for i in range(len(board))
        for j in range(len(board[0]))
        if board[i][j] == 0
    ]


def traverse_path_with_score(pos: Pos, board: Board, visited: Set[Pos]) -> int:
    if pos in visited:
        return 0

    visited.add(pos)

    if board[pos[0]][pos[1]] == 9:
        return 1

    next_positions = build_next_positions(pos, board)
    return sum(
        traverse_path_with_score(next_pos, board, visited)
        for next_pos in next_positions
    )


def traverse_path_with_rating(pos: Pos, board: Board) -> int:
    if board[pos[0]][pos[1]] == 9:
        return 1

    next_positions = build_next_positions(pos, board)
    return sum(
        traverse_path_with_rating(next_pos, board) for next_pos in next_positions
    )


def build_next_positions(pos: Pos, board: Board) -> List[Pos]:
    next_positions = [
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0] - 1, pos[1]),
        (pos[0], pos[1] + 1),
    ]
    return [
        next_pos
        for next_pos in next_positions
        if is_valid_position(next_pos, board)
        and board[next_pos[0]][next_pos[1]] == board[pos[0]][pos[1]] + 1
    ]


def is_valid_position(pos: Pos, board: Board) -> bool:
    return (
        pos[0] >= 0
        and pos[0] < len(board)
        and pos[1] >= 0
        and pos[1] < len(board[pos[0]])
    )


def parse_board(intput: List[str]) -> Board:
    return [[int(e) if isdigit(e) else -1 for e in row] for row in intput]


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
