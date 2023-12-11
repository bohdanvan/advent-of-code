from typing import List, Tuple, TypeVar, TypedDict


class ExtensionMap(TypedDict):
    row_idx_map: List[int]
    col_idx_map: List[int]


Position = Tuple[int, int]


GALAXY_SYMBOL = "#"


T = TypeVar("T")


def main() -> None:
    image = read_input("src/advent_of_code_2023/day11/input.txt")

    print(f"1 -> {solve_part1(image)}")
    print(f"2 -> {solve_part2(image)}")


def solve_part1(image: List[str]) -> int:
    return solve(image, 1)


def solve_part2(image: List[str]):
    return solve(image, 1000000)


def solve(image: List[str], expansion_length) -> int:
    extension_map = createExtensionMap(image, expansion_length)
    galaxies = find_galaxies(image)
    extended_galaxies = [
        (extension_map["row_idx_map"][i], extension_map["col_idx_map"][j])
        for i, j in galaxies
    ]
    extended_galaxies_pairs = create_pairs(extended_galaxies)
    return sum(calc_distance(p[0], p[1]) for p in extended_galaxies_pairs)


def createExtensionMap(image: List[str], expansion_length) -> ExtensionMap:
    row_with_galaxy = [False for i in range(len(image))]
    col_with_galaxy = [False for j in range(len(image[0]))]

    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j] == GALAXY_SYMBOL:
                row_with_galaxy[i] = True
                col_with_galaxy[j] = True

    row_idx_map = [0]
    for i in range(1, len(row_with_galaxy)):
        row_idx_map.append(
            row_idx_map[i - 1] + (1 if row_with_galaxy[i - 1] else expansion_length)
        )

    col_idx_map = [0]
    for j in range(1, len(col_with_galaxy)):
        col_idx_map.append(
            col_idx_map[j - 1] + (1 if col_with_galaxy[j - 1] else expansion_length)
        )

    return ExtensionMap(row_idx_map=row_idx_map, col_idx_map=col_idx_map)


def find_galaxies(image: List[str]) -> List[Position]:
    return [
        (i, j)
        for i in range(len(image))
        for j in range(len(image[i]))
        if image[i][j] == GALAXY_SYMBOL
    ]


def create_pairs(list: List[T]) -> List[Tuple[T, T]]:
    return [
        (list[i], list[j])
        for i in range(len(list) - 1)
        for j in range(i + 1, len(list))
    ]


def calc_distance(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
