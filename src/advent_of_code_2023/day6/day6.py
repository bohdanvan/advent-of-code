from functools import reduce
from operator import mul
from typing import List, TypedDict


class Race(TypedDict):
    time: int
    distance: int


def main() -> None:
    input = read_input("src/advent_of_code_2023/day6/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(input: List[str]) -> int:
    races = parse(input)
    winning_races = [
        calc_winning_races(race["time"], race["distance"]) for race in races
    ]
    return reduce(mul, winning_races, 1)


def solve_part2(input: List[str]) -> int:
    race = parse_part2(input)
    return calc_winning_races(race["time"], race["distance"])


def calc_winning_races(time: int, distance: int) -> int:
    return sum(
        1 for init_time in range(time + 1) if calc_dist(init_time, time) > distance
    )


def calc_dist(init_time: int, time: int) -> int:
    return init_time * (time - init_time)


def parse(lines: List[str]) -> List[Race]:
    times = [int(part) for part in lines[0].replace("Time:", "").strip().split()]
    distances = [
        int(part) for part in lines[1].replace("Distance:", "").strip().split()
    ]

    return [
        Race(time=time, distance=distance) for time, distance in zip(times, distances)
    ]


def parse_part2(lines: List[str]) -> Race:
    return Race(
        time=int(
            "".join(part for part in lines[0].replace("Time:", "").strip().split())
        ),
        distance=int(
            "".join(part for part in lines[1].replace("Distance:", "").strip().split())
        ),
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
