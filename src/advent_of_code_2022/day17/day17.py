from enum import Enum
from typing import List, Tuple
import time

from utils.utils import create_array, deep_copy_matrix


class RockShape(Enum):
    DASH = "####"
    PLUS = """
            .#.
            ###
            .#.
            """
    REV_L = """
            ..#
            ..#
            ###
            """
    COLUMN = """
            #
            #
            #
            #
            """
    SQUARE = """
            ##
            ##
            """


class RockShapes:
    shapes = [
        RockShape.DASH,
        RockShape.PLUS,
        RockShape.REV_L,
        RockShape.COLUMN,
        RockShape.SQUARE,
    ]

    def __init__(self, seed: int = 0) -> None:
        self.i = seed % len(RockShapes.shapes)

    def next(self) -> RockShape:
        res = RockShapes.shapes[self.i]
        self.i = (self.i + 1) % len(RockShapes.shapes)
        return res

    @classmethod
    def shape_pattern(cls, shape: RockShape) -> List[List[bool]]:
        return list(
            reversed(
                [
                    [e == "#" for e in row.strip()]
                    for row in shape.value.split("\n")
                    if len(row.strip()) > 0
                ]
            )
        )


Position = Tuple[int, int]


class Direction(Enum):
    RIGHT = ">"
    LEFT = "<"
    DOWN = "V"


class Directions:
    def __init__(self, directions: List[Direction]) -> None:
        self.directions = directions
        self.i = 0

    def next(self) -> Direction:
        res = self.directions[self.i]
        self.i = (self.i + 1) % len(self.directions)
        return res

    def is_overflow(self) -> bool:
        return self.i == len(self.directions) - 1


class Grid:
    FREE_LAYERS = 7
    CUT_HEIGHT_THRESHOLD = 20

    def __init__(self, play_width: int = 7) -> None:
        self.grid: List[List[bool]] = Grid.create_init_grid(play_width + 2)
        self.height: int = 1
        self.cut_height: int = 0

    @classmethod
    def create_init_grid(cls, width: int) -> List[List[bool]]:
        res = []
        res.append(Grid.create_init_leyer(width))
        for i in range(Grid.FREE_LAYERS):
            res.append(Grid.create_new_leyer(width))
        return res

    @classmethod
    def create_init_leyer(cls, width: int) -> List[bool]:
        return create_array(width, True)

    @classmethod
    def create_new_leyer(cls, width: int) -> List[bool]:
        res = create_array(width, False)
        res[0] = res[-1] = True
        return res

    def extend(self) -> None:
        new_layers = max(
            self.height + Grid.FREE_LAYERS - (len(self.grid) + self.cut_height), 0
        )
        for _ in range(new_layers):
            self.grid.append(Grid.create_new_leyer(self.get_width()))

    def cut_grid(self) -> None:
        if len(self.grid) <= 3 * Grid.CUT_HEIGHT_THRESHOLD:
            return
        self.cut_height += Grid.CUT_HEIGHT_THRESHOLD
        self.grid = self.grid[Grid.CUT_HEIGHT_THRESHOLD :]

    def get_width(self) -> int:
        return len(self.grid[0])

    def get_height(self) -> int:
        return self.height

    def draw_with_rock(self, shape: RockShape, pos: Position) -> str:
        grid_copy = deep_copy_matrix(self.grid)
        self.__apply_rock_on_grid(grid_copy, shape, pos)
        return Grid.draw_grid(grid_copy)

    def is_valid(self, shape: RockShape, pos: Position) -> bool:
        shape_pattern = RockShapes.shape_pattern(shape)

        grid_i = pos[0] - self.cut_height
        for shape_i in range(len(shape_pattern)):
            grid_j = pos[1]
            for shape_j in range(len(shape_pattern[0])):
                if shape_pattern[shape_i][shape_j] and self.grid[grid_i][grid_j]:
                    return False
                grid_j += 1
            grid_i += 1

        return True

    def apply_rock(self, shape: RockShape, pos: Position) -> None:
        self.__apply_rock_on_grid(self.grid, shape, pos)
        shape_pattern = RockShapes.shape_pattern(shape)
        self.height = max(self.height, pos[0] + len(shape_pattern))
        self.extend()
        self.cut_grid()

    def __apply_rock_on_grid(
        self, grid: List[List[bool]], shape: RockShape, pos: Position
    ) -> None:
        shape_pattern = RockShapes.shape_pattern(shape)

        grid_i = pos[0] - self.cut_height
        for shape_i in range(len(shape_pattern)):
            grid_j = pos[1]
            for shape_j in range(len(shape_pattern[0])):
                if shape_pattern[shape_i][shape_j]:
                    grid[grid_i][grid_j] = True
                grid_j += 1
            grid_i += 1

    @classmethod
    def draw_grid(cls, grid: List[List[bool]]) -> str:
        return "\n".join(
            [
                "".join("#" if grid[i][j] else "." for j in range(len(grid[0])))
                for i in reversed(range(len(grid)))
            ]
        )

    def __repr__(self) -> str:
        return Grid.draw_grid(self.grid)


def main() -> None:
    input = read_input("src/advent_of_code_2022/day17/input.txt")

    directions = parse(input[0])

    print(f"1 -> {solve_part1(directions, 1875)}")
    # print(f"1 -> {solve_part1(directions, 1000000000000)}")
    # print(f"2 -> {solve_part2()}")


def parse(input: str) -> Directions:
    return Directions([Direction(s) for s in input])


def solve_part1(directions: Directions, rocks: int) -> int:
    shapes = RockShapes()
    grid = Grid()

    for i in range(rocks):
        shape = shapes.next()
        run_fall(grid, shape, directions)

        if directions.is_overflow():
            print(
                f"///////////////////////////////// i = {i} -> {grid.get_height() - 1}{' [Overflow]' if directions.is_overflow() else ''}"
            )
            print(f"====================== {i} ============================")
            print(grid)

    return grid.get_height() - 1


def run_fall(grid: Grid, shape: RockShape, directions: Directions) -> None:
    pos = (grid.get_height() + 3, 3)

    print_grid(grid, shape, pos)

    while True:
        direction = directions.next()
        new_pos = move(pos, direction)
        if grid.is_valid(shape, new_pos):
            pos = new_pos
        print_grid(grid, shape, pos)

        direction = Direction.DOWN
        new_pos = move(pos, direction)
        if grid.is_valid(shape, new_pos):
            pos = new_pos
        else:
            break
        print_grid(grid, shape, pos)

    grid.apply_rock(shape, pos)


def print_grid(grid: Grid, shape: RockShape, pos: Position):
    pass
    # print(grid.draw_with_rock(shape, pos))
    # print("---------------------------------------------------")


def move(pos: Position, direction: Direction) -> Position:
    match direction:
        case Direction.DOWN:
            return (pos[0] - 1, pos[1])
        case Direction.LEFT:
            return (pos[0], pos[1] - 1)
        case Direction.RIGHT:
            return (pos[0], pos[1] + 1)


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
