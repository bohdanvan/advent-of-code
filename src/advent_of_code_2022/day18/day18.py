from __future__ import annotations
from typing import List, Tuple

from utils.utils import create_3d_grid, flatten

DIMENSIONS = 3

Point = Tuple[int, int, int]


class Search3D:
    @classmethod
    def create(cls, points: List[Point]) -> Search3D:
        max_point = [max([p[d] for p in points]) for d in range(DIMENSIONS)]
        search3D = Search3D(max_point)
        for p in points:
            search3D.add(p)
        return search3D

    def __init__(self, max_point: Point) -> None:
        self.grid: List[List[List[bool]]] = create_3d_grid(
            x_size=max_point[0] + 1,
            y_size=max_point[1] + 1,
            z_size=max_point[2] + 1,
            filler=False,
        )

    def add(self, p: Point) -> None:
        self.grid[p[0]][p[1]][p[2]] = True

    def is_valid(self, p: Point) -> bool:
        return not (
            p[0] < 0
            or p[0] >= len(self.grid)
            or p[1] < 0
            or p[1] >= len(self.grid[0])
            or p[2] < 0
            or p[2] >= len(self.grid[0][0])
        )

    def contains(self, p: Point) -> bool:
        if not self.is_valid(p):
            return False

        return self.grid[p[0]][p[1]][p[2]]


def main() -> None:
    input = read_input("src/advent_of_code_2022/day18/input.txt")

    points = parse(input)

    print(f"1 -> {solve_part1(points)}")
    print(f"2 -> {solve_part2(points)}")


def parse(input: List[str]) -> List[Point]:
    return [tuple([int(x) for x in line.split(",")]) for line in input]


def solve_part1(points: List[Point]):
    search3D = Search3D.create(points)

    total_surface = 0
    for p in points:
        existing_neighbours = [n for n in neighbours(p) if search3D.contains(n)]

        total_surface += 6 - len(existing_neighbours)

    return total_surface


def inc_in_dimension(point: Point, inc: int, dimension: int) -> Point:
    new_point = list(point).copy()
    new_point[dimension] += inc
    return tuple(new_point)


def solve_part2(points: List[Point]):
    # BFS on air

    search3D = Search3D.create(points)

    visited_air = set()
    visited_border = set()
    candidates = set([tuple([0, 0, 0])])

    while len(candidates) > 0:
        p = candidates.pop()

        is_air = not search3D.contains(p)

        if is_air:
            visited_air.add(p)

            valid_neighbours = [
                n
                for n in neighbours(p)
                if search3D.is_valid(n)
                and n not in visited_air
                and n not in visited_border
            ]

            candidates.update(valid_neighbours)
        else:
            visited_border.add(p)

    total_surface = 0
    for p in visited_border:
        air_neighbours = [
            n for n in neighbours(p) if not search3D.is_valid(n) or n in visited_air
        ]

        total_surface += len(air_neighbours)

    return total_surface


def neighbours(p: Point) -> List[Point]:
    return flatten(
        [
            [inc_in_dimension(p, 1, d), inc_in_dimension(p, -1, d)]
            for d in range(DIMENSIONS)
        ]
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
