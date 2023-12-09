from typing import List, Tuple


def main() -> None:
    rows = read_input("src/advent_of_code_2023/day9/input.txt")

    print(f"1 -> {solve_part1(rows)}")
    print(f"2 -> {solve_part2(rows)}")


def solve_part1(rows: List[List[int]]) -> int:
    return sum(find_next(row) for row in rows)


def solve_part2(rows: List[List[int]]) -> int:
    return sum(find_prev(row) for row in rows)


def find_next(a: List[int]) -> int:
    return sum(find_first_last_diff_elems(a)[1])


def find_prev(a: List[int]) -> int:
    first_diff_elems = find_first_last_diff_elems(a)[0]

    res = 0
    for elem in reversed(first_diff_elems):
        res = elem - res

    return res


def find_first_last_diff_elems(a: List[int]) -> Tuple[List[int], List[int]]:
    first_diff_elems = [a[0]]
    last_diff_elems = [a[-1]]
    curr = a
    diff = []

    should_continue = True
    while len(curr) > 1 and should_continue:
        should_continue = False

        for i in range(1, len(curr)):
            diff_elem = curr[i] - curr[i - 1]
            diff.append(diff_elem)
            should_continue = should_continue or (diff_elem != 0)

        first_diff_elems.append(diff[0])
        last_diff_elems.append(diff[-1])
        curr = diff
        diff = []

    if len(curr) == 1:
        first_diff_elems.append(curr[0])
        last_diff_elems.append(curr[0])

    return (first_diff_elems, last_diff_elems)


def read_input(file_name: str) -> List[List[int]]:
    with open(file_name) as f:
        return [[int(n) for n in line.split(" ")] for line in f]


if __name__ == "__main__":
    main()
