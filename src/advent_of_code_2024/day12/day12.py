from dataclasses import dataclass, field
from typing import List, Set, Tuple, cast

from more_itertools import map_reduce

Board = List[str]
Pos = Tuple[int, int]


@dataclass
class Region:
    symbol: str
    area: int = 0
    horizontal_sides: List[Pos] = field(default_factory=list)
    vertical_sides: List[Pos] = field(default_factory=list)

    def perimeter(self) -> int:
        return len(self.horizontal_sides) + len(self.vertical_sides)

    def count_unique_sides(self) -> int:
        # Dict[int, List[int]]
        horizontal_sides_dict = map_reduce(
            self.horizontal_sides,
            keyfunc=lambda side: side[0],
            valuefunc=lambda side: side[1],
        )
        count_unique_horizontal_sides = sum(
            count_sequences(sides, self.build_vertical_breaks(row))
            for row, sides in horizontal_sides_dict.items()
        )

        vertical_sides_dict = map_reduce(
            self.vertical_sides,
            keyfunc=lambda side: side[1],
            valuefunc=lambda side: side[0],
        )
        count_unique_vertical_sides = sum(
            count_sequences(sides, self.build_horizontal_breaks(col))
            for col, sides in vertical_sides_dict.items()
        )

        return count_unique_vertical_sides + count_unique_horizontal_sides

    def build_vertical_breaks(self, row: int) -> Set[int]:
        return {side[1] for side in self.vertical_sides if side[0] == row}.intersection(
            {side[1] for side in self.vertical_sides if side[0] == row - 1}
        )

    def build_horizontal_breaks(self, col: int) -> Set[int]:
        return {
            side[0] for side in self.horizontal_sides if side[1] == col
        }.intersection(
            {side[0] for side in self.horizontal_sides if side[1] == col - 1}
        )


POS_INC = [
    (0, +1),
    (0, -1),
    (+1, 0),
    (-1, 0),
]


def main() -> None:
    input = read_input("src/advent_of_code_2024/day12/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(board: Board) -> int:
    regions = traverse(board)

    return sum(region.perimeter() * region.area for region in regions)


def solve_part2(board: Board) -> int:
    regions = traverse(board)

    # for region in regions:
    #     unique_sides = region.count_unique_sides()
    #     print(
    #         f"A region of {region.symbol} plants with price {region.area} * {unique_sides} = {region.area * unique_sides}."
    #     )

    return sum(region.count_unique_sides() * region.area for region in regions)


def traverse(board: Board) -> List[Region]:
    visited = [[False for _ in range(len(board[0]))] for _ in range(len(board))]

    regions: List[Region] = []
    next_region_candidates: Set[Pos] = set([(0, 0)])

    while next_region_candidates:
        (next_region_i, next_region_j) = next_region_candidates.pop()

        if visited[next_region_i][next_region_j]:
            continue

        region_candidates: Set[Pos] = set([(next_region_i, next_region_j)])
        region = Region(board[next_region_i][next_region_j])
        while region_candidates:
            (i, j) = region_candidates.pop()

            if visited[i][j]:
                continue

            visited[i][j] = True

            neighbors = next_valid_positions((i, j), board)
            same_region_neighbors = set(
                (next_i, next_j)
                for (next_i, next_j) in neighbors
                if board[next_i][next_j] == region.symbol
            )
            different_region_neighbors = set(
                (next_i, next_j)
                for (next_i, next_j) in neighbors
                if board[next_i][next_j] != region.symbol
            )

            region.area += 1
            if (i - 1, j) not in same_region_neighbors:
                region.horizontal_sides.append((i, j))
            if (i + 1, j) not in same_region_neighbors:
                region.horizontal_sides.append((i + 1, j))
            if (i, j - 1) not in same_region_neighbors:
                region.vertical_sides.append((i, j))
            if (i, j + 1) not in same_region_neighbors:
                region.vertical_sides.append((i, j + 1))

            region_candidates.update(same_region_neighbors)
            next_region_candidates.update(different_region_neighbors)

        regions.append(region)
    return regions


def count_sequences(a: List[int], breaks: Set[int]) -> int:
    a.sort()

    seq_count = 1
    for i in range(1, len(a)):
        if a[i] != a[i - 1] + 1 or a[i] in breaks:
            seq_count += 1

    return seq_count


def next_valid_positions(pos: Pos, board: Board) -> List[Pos]:
    next_positions = [pos_sum(pos, pos_inc) for pos_inc in POS_INC]
    return [pos for pos in next_positions if is_valid_pos(pos, board)]


def is_valid_pos(pos: Pos, board: Board) -> bool:
    (i, j) = pos
    return i >= 0 and i < len(board) and j >= 0 and j < len(board[i])


def pos_sum(a: Pos, b: Pos) -> Pos:
    return cast(Pos, tuple(list(map(sum, zip(a, b)))))


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
