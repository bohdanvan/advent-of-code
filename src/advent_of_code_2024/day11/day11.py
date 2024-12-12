from collections import defaultdict
from typing import Counter, Dict, List


def main() -> None:
    input = read_input("src/advent_of_code_2024/day11/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(list: List[int]) -> int:
    return solve(list, 25)


def solve_part2(list: List[int]) -> int:
    return solve(list, 75)


def solve(list: List[int], loops: int) -> int:
    counter: Dict[int, int] = Counter(list)

    for _ in range(loops):
        next_counter: Dict[int, int] = defaultdict(int)

        for n, count in counter.items():
            if n == 0:
                next_counter[1] += count
            elif len(str(n)) % 2 == 0:
                s = str(n)
                left = int(s[0 : len(s) // 2])
                right = int(s[len(s) // 2 :])
                next_counter[left] += count
                next_counter[right] += count
            else:
                next_counter[n * 2024] += count

            counter = next_counter

    return sum(counter.values())


def read_input(file_name: str) -> List[int]:
    with open(file_name) as f:
        return [int(part) for part in f.readline().strip("\n").split()]


if __name__ == "__main__":
    main()
