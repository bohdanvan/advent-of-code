from typing import List


def main() -> None:
    matrix = read_input("src/advent_of_code_2024/day4/input.txt")

    print(f"1 -> {solve_part1(matrix)}")
    print(f"2 -> {solve_part2(matrix)}")


def solve_part1(matrix: List[str]) -> int:
    count_in_rows = count_xmax_in_matrix(matrix)
    count_in_cols = count_xmax_in_matrix(transpose(matrix))
    count_in_desc_diagonals = count_xmax_in_matrix(to_desc_diagonals(matrix))
    count_in_asc_diagonals = count_xmax_in_matrix(to_asc_diagonals(matrix))
    return (
        count_in_rows + count_in_cols + count_in_desc_diagonals + count_in_asc_diagonals
    )


def count_xmax_in_matrix(matrix: List[str]) -> int:
    return sum(count_xmax(row) for row in matrix)


def count_xmax(s: str) -> int:
    return s.count("XMAS") + s.count("SAMX")


def transpose(matrix: List[str]) -> List[str]:
    return [
        "".join(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0]))
    ]


def to_desc_diagonals(matrix: List[str]) -> List[str]:
    res: List[List[str]] = []

    diagonal: List[str]
    for j_idx in range(len(matrix[0]) - 1, 0, -1):
        diagonal = []
        i, j = 0, j_idx
        while is_valid_index(i, j, matrix):
            diagonal.append(matrix[i][j])
            i, j = i + 1, j + 1
        res.append(diagonal)

    for i_idx in range(0, len(matrix)):
        diagonal = []
        i, j = i_idx, 0
        while is_valid_index(i, j, matrix):
            diagonal.append(matrix[i][j])
            i, j = i + 1, j + 1
        res.append(diagonal)

    return ["".join(row) for row in res]


def to_asc_diagonals(matrix: List[str]) -> List[str]:
    res: List[List[str]] = []

    diagonal: List[str]
    for i_idx in range(0, len(matrix)):
        diagonal = []
        i, j = i_idx, 0
        while is_valid_index(i, j, matrix):
            diagonal.append(matrix[i][j])
            i, j = i - 1, j + 1
        res.append(diagonal)

    for j_idx in range(1, len(matrix[0])):
        diagonal = []
        i, j = len(matrix) - 1, j_idx
        while is_valid_index(i, j, matrix):
            diagonal.append(matrix[i][j])
            i, j = i - 1, j + 1
        res.append(diagonal)

    return ["".join(row) for row in res]


def is_valid_index(i: int, j: int, matrix: List[str]) -> bool:
    return i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix[0])


def solve_part2(matrix: List[str]) -> int:
    res: int = 0

    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[0]) - 1):
            if matrix[i][j] != "A":
                continue

            x_str = (
                matrix[i - 1][j - 1]
                + matrix[i][j]
                + matrix[i + 1][j + 1]
                + "."
                + matrix[i - 1][j + 1]
                + matrix[i][j]
                + matrix[i + 1][j - 1]
            )
            if x_str in ["MAS.MAS", "MAS.SAM", "SAM.MAS", "SAM.SAM"]:
                res += 1

    return res


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
