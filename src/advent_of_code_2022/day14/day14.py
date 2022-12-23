from typing import List, Tuple, TypedDict

from utils.utils import create_matrix, flatten

Position = Tuple[int, int]
Path = List[Position]

SAND_START_POS = (500, 0)
PRINT_STEP = 50


class PositionStats(TypedDict):
    offset_x: int
    offset_y: int
    grid_rows: int
    grid_cols: int
    min_x: int
    max_x: int
    min_y: int
    max_y: int


class Grid:
    def __init__(self, rows: int, cols: int) -> None:
        self.grid: List[List[bool]] = create_matrix(rows, cols, False)
        self.height: int = 1
        self.cut_height: int = 0

    def add_path(self, path: Path) -> None:
        for i in range(1, len(path)):
            self.add_line(path[i - 1], path[i])

    def add_line(self, pos1: Position, pos2: Position) -> None:
        if pos1[0] == pos2[0]:
            x = pos1[0]
            for y in range(min(pos1[1], pos2[1]), max(pos1[1], pos2[1]) + 1):
                self.grid[y][x] = True
        elif pos1[1] == pos2[1]:
            y = pos1[1]
            for x in range(min(pos1[0], pos2[0]), max(pos1[0], pos2[0]) + 1):
                self.grid[y][x] = True
        else:
            raise AssertionError("Unsupported line")

    def test(self, x: int, y: int) -> bool:
        return self.grid[y][x]

    def apply(self, x: int, y: int) -> None:
        self.grid[y][x] = True

    def is_abyss(self, x: int, y: int) -> bool:
        return x == 0 or x == len(self.grid[0]) or y == len(self.grid) - 1

    def is_top(self, x: int, y: int) -> bool:
        return y == 0

    def draw(self) -> str:
        return "\n".join(
            [
                "".join(
                    "#" if self.grid[i][j] else "." for j in range(len(self.grid[0]))
                )
                for i in range(len(self.grid))
            ]
        )


def main() -> None:
    input = read_input("src/advent_of_code_2022/day14/input.txt")

    paths = parse(input)

    print(f"1 -> {solve_part1(paths)}")
    print(f"2 -> {solve_part2(paths, 200)}")


def solve_part1(paths: List[Path]):
    pos_stats = calc_position_stats(paths)
    paths = adjust_paths(paths, pos_stats)
    grid = Grid(pos_stats["grid_rows"], pos_stats["grid_cols"])

    for path in paths:
        grid.add_path(path)

    print(grid.draw())
    print("----------------------")

    sand_start_pos = adjust_pos(SAND_START_POS, pos_stats)
    count = 0

    pos = fall_sand(grid, sand_start_pos)
    while not grid.is_abyss(pos[0], pos[1]):
        grid.apply(pos[0], pos[1])
        count += 1
        if count % PRINT_STEP == 0:
            print(grid.draw())
            print("----------------------")

        pos = fall_sand(grid, sand_start_pos)

    return count


def solve_part2(paths: List[Path], floor_adjustment: int):
    pos_stats = calc_position_stats(paths)
    floor = [
        (pos_stats["min_x"] - floor_adjustment, pos_stats["max_y"] + 2),
        (pos_stats["max_x"] + floor_adjustment, pos_stats["max_y"] + 2),
    ]
    paths.append(floor)

    pos_stats = calc_position_stats(paths)
    paths = adjust_paths(paths, pos_stats)
    grid = Grid(pos_stats["grid_rows"], pos_stats["grid_cols"])

    for path in paths:
        grid.add_path(path)

    print(grid.draw())
    print("----------------------")

    sand_start_pos = adjust_pos(SAND_START_POS, pos_stats)
    count = 0
    pos = (1, 1) # dummy
    while not grid.is_top(pos[0], pos[1]):
        pos = fall_sand(grid, sand_start_pos)
        
        grid.apply(pos[0], pos[1])
        count += 1
        if count % PRINT_STEP == 0:
            print(grid.draw())
            print("----------------------")

    return count


def fall_sand(grid: Grid, start_pos: Position) -> Position:
    pos = start_pos

    while True:
        next_pos = next_sand_pos(grid, pos)
        if next_pos == pos or grid.is_abyss(next_pos[0], next_pos[1]):
            return next_pos
        pos = next_pos


def next_sand_pos(grid: Grid, pos: Position) -> Position:
    if not grid.test(pos[0], pos[1] + 1):
        return (pos[0], pos[1] + 1)
    if not grid.test(pos[0] - 1, pos[1] + 1):
        return (pos[0] - 1, pos[1] + 1)
    if not grid.test(pos[0] + 1, pos[1] + 1):
        return (pos[0] + 1, pos[1] + 1)
    return pos


def parse_position(s: str) -> Position:
    tokens = [int(e) for e in s.strip().split(",")]
    return (tokens[0], tokens[1])


def calc_position_stats(paths: List[Path]) -> PositionStats:
    xs = flatten([[pos[0] for pos in path] for path in paths])
    ys = flatten([[pos[1] for pos in path] for path in paths])

    min_x = min(xs)
    max_x = max(xs)

    min_y = min(ys)
    max_y = max(ys)

    return {
        "offset_x": min_x - 1,
        "offset_y": 0,
        "grid_rows": max_y + 2,
        "grid_cols": max_x - min_x + 3,
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y,
    }


def adjust_paths(paths: List[Path], pos_stats: PositionStats) -> List[Path]:
    return [[adjust_pos(pos, pos_stats) for pos in path] for path in paths]


def adjust_pos(pos: Position, pos_stats: PositionStats) -> Position:
    return (pos[0] - pos_stats["offset_x"], pos[1] - pos_stats["offset_y"])


def parse(input: List[str]) -> List[Path]:
    return [parse_path(line) for line in input]


def parse_path(s: str) -> Path:
    return [parse_position(pos_str) for pos_str in s.strip().split("->")]


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
