from collections import deque
from functools import partial
from operator import is_not
from typing import List, Optional, Set, Tuple, TypeVar, TypedDict


Point = Tuple[int, int]


class ClimbingInput(TypedDict):
    start: Point
    end: Point
    grid: List[List[int]]


def main() -> None:
    input = read_input("src/advent_of_code_2022/day12/input.txt")
    climbing_input = parse(input)

    print(
        f"1 -> {solve_part1(climbing_input['grid'], climbing_input['start'], climbing_input['end'])}"
    )
    print(
        f"2 -> {solve_part2(climbing_input['grid'], climbing_input['start'], climbing_input['end'])}"
    )


def solve_part1(grid: List[List[int]], start: Point, end: Point) -> Optional[int]:
    visited_grid: List[List[bool]] = create_matrix(len(grid), len(grid[0]), False)
    steps_grid: List[List[int]] = create_matrix(len(grid), len(grid[0]), -1)

    candidates: Set[Point] = {start}

    steps = 0
    while len(candidates) > 0:
        next_candidates: Set[Point] = set()

        for p in candidates:
            visited_grid[p[0]][p[1]] = True
            steps_grid[p[0]][p[1]] = steps
            if p == end:
                return steps

            curr_height = grid[p[0]][p[1]]

            neighbours = [
                (p[0] + 1, p[1]),
                (p[0] - 1, p[1]),
                (p[0], p[1] + 1),
                (p[0], p[1] - 1),
            ]
            neighbours = [
                n
                for n in neighbours
                if n[0] >= 0
                and n[0] < len(grid)
                and n[1] >= 0
                and n[1] < len(grid[0])
                and grid[n[0]][n[1]] <= curr_height + 1
                and visited_grid[n[0]][n[1]] == False
            ]
            next_candidates.update(neighbours)

        # if steps % 5 == 0:
        #     print_steps_grid(steps_grid)

        candidates = next_candidates

        steps += 1

    return None


def solve_part2(grid: List[List[int]], start: Point, end: Point) -> int:
    all_starts: List[Point] = [
        (i, j)
        for (i, row) in enumerate(grid)
        for (j, e) in enumerate(row)
        if chr(e) == "a"
    ] + [start]

    return min(
        [
            res
            for res in [solve_part1(grid, s, end) for s in all_starts]
            if res is not None
        ]
    )


def print_steps_grid(grid: List[List[int]]) -> None:
    for row in grid:
        print("".join([f"{e:3}" if e >= 0 else "  ." for e in row]))
    print("----------------")


def parse(input: List[str]) -> ClimbingInput:
    grid = create_matrix(len(input), len(input[0]), 0)

    start = None
    end = None
    for (i, row) in enumerate(input):
        for (j, e) in enumerate(row):
            if e == "S":
                start = (i, j)
                e = "a"
            elif e == "E":
                end = (i, j)
                e = "z"

            grid[i][j] = ord(e)

    if not start:
        raise AssertionError()
    if not end:
        raise AssertionError()

    return {
        "start": start,
        "end": end,
        "grid": grid,
    }


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


T = TypeVar("T")


def create_matrix(rows: int, cols: int, filler: T) -> List[List[T]]:
    return [[filler for _ in range(cols)] for _ in range(rows)]


if __name__ == "__main__":
    main()
