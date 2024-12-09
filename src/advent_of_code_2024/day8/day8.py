from collections import defaultdict
from typing import Dict, List, Set, Tuple

Board = List[str]
Pos = Tuple[int, int]


def main() -> None:
    input = read_input("src/advent_of_code_2024/day8/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(board: Board) -> int:
    return solve(board, "part1")


# 1147 - too low
def solve_part2(board: Board):
    return solve(board, "part2")


def solve(board: Board, stategy: str) -> int:
    antennas = find_antennas(board)

    antinodes = set()
    for _, nodes in antennas.items():
        antinodes.update(create_frequency_antinodes(nodes, board, stategy))

    # print(sorted(antinodes, key=lambda p: (p[0], p[1])))

    return len(antinodes)


def create_frequency_antinodes(
    nodes: List[Pos], board: Board, stategy: str
) -> Set[Pos]:
    antinodes: Set[Pos] = set()
    for i in range(len(nodes) - 1):
        for j in range(i + 1, len(nodes)):
            antinodes.update(create_antinodes(nodes[i], nodes[j], board, stategy))
            antinodes.update(create_antinodes(nodes[j], nodes[i], board, stategy))

    return antinodes


def create_antinodes(a: Pos, b: Pos, board: Board, stategy: str) -> List[Pos]:
    if stategy == "part1":
        antinode = create_antinode(a, b)
        return [antinode] if is_valid_pos(antinode, board) else []
    elif stategy == "part2":
        antinodes = [a, b]
        antinode = create_antinode(a, b)
        while is_valid_pos(antinode, board):
            antinodes.append(antinode)
            a, b = antinode, a
            antinode = create_antinode(a, b)

        return antinodes
    else:
        raise AssertionError(f"Invalid strategy: {stategy}")


def create_antinode(a: Pos, b: Pos) -> Pos:
    return (2 * a[0] - b[0], 2 * a[1] - b[1])


def is_valid_pos(pos: Pos, board: Board) -> bool:
    return (
        pos[0] >= 0
        and pos[0] < len(board)
        and pos[1] >= 0
        and pos[1] < len(board[pos[0]])
    )


def find_antennas(board: Board) -> Dict[str, List[Pos]]:
    antennas = defaultdict(lambda: list())
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != ".":
                antennas[board[i][j]].append((i, j))
    return antennas


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
