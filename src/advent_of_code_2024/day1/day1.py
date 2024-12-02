from typing import Counter, List, Tuple


def main() -> None:
    lines = read_input("src/advent_of_code_2024/day1/input.txt")

    print(f"1 -> {solve_part1(lines)}")
    print(f"2 -> {solve_part2(lines)}")


def solve_part1(input: List[str]) -> int:
    (left, right) = parse(input)

    left.sort()
    right.sort()

    return sum(map(lambda pair: abs(pair[0] - pair[1]), zip(left, right)))


def solve_part2(input: List[str]) -> int:
    (left, right) = parse(input)

    right_counter = Counter(right)

    return sum(map(lambda e: e * right_counter.get(e, 0), left))


def parse(lines: List[str]) -> Tuple[List[int], List[int]]:
    (left, right) = map(list, zip(*(map(int, s.split()) for s in lines)))
    return (left, right)


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
