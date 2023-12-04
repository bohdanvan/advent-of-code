import re
from typing import List, TypedDict, Optional, TypeVar


class ColorCount(TypedDict):
    red: int
    green: int
    blue: int


BASE_COLOR_COUNT = ColorCount(red=12, green=13, blue=14)


def main() -> None:
    lines = read_input("src/advent_of_code_2023/day2/input.txt")

    print(f"1 -> {solve_part1(lines)}")
    print(f"2 -> {solve_part2(lines)}")


def solve_part1(lines: List[str]) -> int:
    result = 0
    game_id = 1
    for line in lines:
        color_counts = parse_color_counts(line)
        if is_valid_color_count(max_color_count(color_counts)):
            result += game_id
        game_id += 1
    return result


def solve_part2(lines: List[str]) -> int:
    result = 0
    game_id = 1
    for line in lines:
        color_counts = parse_color_counts(line)
        color_count_max = max_color_count(color_counts)
        result += (
            color_count_max["red"] * color_count_max["green"] * color_count_max["blue"]
        )
        game_id += 1
    return result


def parse_color_counts(s: str) -> List[ColorCount]:
    s = regex_search(r"^Game [\d]*: (.*)$", s)
    return [parse_color_count(part.strip()) for part in s.split(";")]


def parse_color_count(s: str) -> ColorCount:
    return ColorCount(
        red=int(or_default(maybe_regex_search(r"(\d*) red", s), "0")),
        green=int(or_default(maybe_regex_search(r"(\d*) green", s), "0")),
        blue=int(or_default(maybe_regex_search(r"(\d*) blue", s), "0")),
    )


def max_color_count(list: List[ColorCount]) -> ColorCount:
    return ColorCount(
        red=max([c["red"] for c in list]),
        green=max([c["green"] for c in list]),
        blue=max([c["blue"] for c in list]),
    )


def is_valid_color_count(color_count: ColorCount) -> bool:
    return (
        color_count["red"] <= BASE_COLOR_COUNT["red"]
        and color_count["green"] <= BASE_COLOR_COUNT["green"]
        and color_count["blue"] <= BASE_COLOR_COUNT["blue"]
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


def regex_search(pattern: str, s: str, group: int = 1) -> str:
    match = maybe_regex_search(pattern, s, group)
    if match is None:
        raise AssertionError
    return match


def maybe_regex_search(pattern: str, s: str, group: int = 1) -> Optional[str]:
    match = re.search(pattern, s.strip())
    if not match:
        return None
    return match.group(group)


T = TypeVar("T")


def or_default(x: Optional[T], default_value: T) -> T:
    return x if x is not None else default_value


if __name__ == "__main__":
    main()
