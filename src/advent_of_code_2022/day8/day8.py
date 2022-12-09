from typing import List


def main() -> None:
    input = read_input("src/advent_of_code_2022/day8/input.txt")
    grid = parse_intput(input)

    print(f"1 -> {solve_part1(grid)}")
    print(f"2 -> {solve_part2(grid)}")


def parse_intput(input: List[str]) -> List[List[int]]:
    return [[int(ch) for ch in line] for line in input]


def solve_part1(grid: List[List[int]]) -> int:
    # O(N^2)

    rows = len(grid)
    cols = len(grid[0])

    left_prefix_max = create_matrix(rows, cols, 100)
    for i in range(rows):
        for j in range(cols):
            left_prefix_max[i][j] = (
                max(left_prefix_max[i][j - 1], grid[i][j]) if j != 0 else grid[i][j]
            )

    right_prefix_max = create_matrix(rows, cols, 100)
    for i in range(rows):
        for j in reversed(range(cols)):
            right_prefix_max[i][j] = (
                max(right_prefix_max[i][j + 1], grid[i][j])
                if j != cols - 1
                else grid[i][j]
            )

    top_prefix_max = create_matrix(rows, cols, 100)
    for i in range(rows):
        for j in range(cols):
            top_prefix_max[i][j] = (
                max(top_prefix_max[i - 1][j], grid[i][j]) if i != 0 else grid[i][j]
            )

    bottom_prefix_max = create_matrix(rows, cols, 100)
    for i in reversed(range(rows)):
        for j in range(cols):
            bottom_prefix_max[i][j] = (
                max(bottom_prefix_max[i + 1][j], grid[i][j])
                if i != rows - 1
                else grid[i][j]
            )

    res = 0
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            boundaries = [
                left_prefix_max[i][j - 1],
                right_prefix_max[i][j + 1],
                top_prefix_max[i - 1][j],
                bottom_prefix_max[i + 1][j],
            ]
            if any([grid[i][j] > boundary for boundary in boundaries]):
                res += 1

    res += 2 * len(grid) + 2 * (len(grid[0]) - 2)
    return res


def create_matrix(rows: int, cols: int, val: int) -> List[List[int]]:
    return [[val] * cols for _ in range(rows)]


def solve_part2(grid: List[List[int]]):
    # O(N^4)

    rows = len(grid)
    cols = len(grid[0])

    max_score = 0

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            val = grid[i][j]

            left_score = 0
            for k in reversed(range(0, j)):
                left_score += 1
                if grid[i][k] >= val:
                    break

            righ_score = 0
            for k in range(j + 1, cols):
                righ_score += 1
                if grid[i][k] >= val:
                    break

            top_score = 0
            for k in reversed(range(0, i)):
                top_score += 1
                if grid[k][j] >= val:
                    break

            bottom_score = 0
            for k in range(i + 1, rows):
                bottom_score += 1
                if grid[k][j] >= val:
                    break

            total_score = left_score * righ_score * top_score * bottom_score

            max_score = max(max_score, total_score)
            
            # print(f"({i}, {j}) -> (L = {left_score}, R = {righ_score}, T = {top_score}, B = {bottom_score}")

    return max_score


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
