import re
from typing import Dict, List, Tuple, TypedDict
from functools import reduce


def main() -> None:
    input = read_input("src/advent_of_code_2023/day8/input.txt")
    path = input[0]
    directions = {
        d[0]: (d[1], d[2]) for d in [parse_direction(line) for line in input[2::]]
    }

    print(f"1 -> {solve_part1(path, directions)}")
    print(f"2 -> {solve_part2(path, directions)}")


def solve_part1(path: str, directions: Dict[str, Tuple[str, str]]) -> int:
    node = "AAA"

    path_idx = 0
    count = 0
    while node != "ZZZ":
        if path[path_idx] == "L":
            node = directions[node][0]
        else:
            node = directions[node][1]

        path_idx = (path_idx + 1) % len(path)
        count += 1

    return count


def solve_part2(path: str, directions: Dict[str, Tuple[str, str]]) -> int:
    nodes = [n for n in directions.keys() if n[2] == "A"]
    end_node_steps: List[int] = [0 for i in range(len(nodes))]

    path_idx = 0
    count = 0
    while not all(s > 0 for s in end_node_steps):
        count += 1

        for i in range(len(nodes)):
            if path[path_idx] == "L":
                nodes[i] = directions[nodes[i]][0]
            else:
                nodes[i] = directions[nodes[i]][1]

            if nodes[i][2] == "Z" and end_node_steps[i] == 0:
                end_node_steps[i] = count

        path_idx = (path_idx + 1) % len(path)

    return compute_lcm_list(end_node_steps)


def compute_lcm_list(list: List[int]) -> int:
    return reduce(lambda x, y: compute_lcm(x, y), list, 1)


def compute_gcd(x, y):
    """Greatest Common Divisor"""
    while y:
        x, y = y, x % y
    return x


def compute_lcm(x, y):
    """Least Common Multiple"""
    lcm = (x * y) // compute_gcd(x, y)
    return lcm


def parse_direction(s: str) -> Tuple[str, str, str]:
    match = re.search("(.+) = \((.*), (.*)\)", s.strip())
    if match is None:
        raise AssertionError(f"Not recognised line: {s}")
    return (match.group(1), match.group(2), match.group(3))


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
