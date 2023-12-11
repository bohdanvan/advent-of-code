from functools import reduce
from itertools import chain
from typing import Dict, List, Optional, Set, Tuple, TypeVar, TypedDict


class AlmanacRange(TypedDict):
    dest_start: int
    source_start: int
    len: int


class SourceRange(TypedDict):
    start: int
    len: int


AlmanacMap = List[AlmanacRange]


class Almanac(TypedDict):
    seeds: List[int]
    almanac_maps: List[AlmanacMap]


class AlmanacPart2(TypedDict):
    seed_ranges: List[SourceRange]
    almanac_maps: List[AlmanacMap]


def main() -> None:
    lines = read_input("src/advent_of_code_2023/day5/input.txt")

    print(f"1 -> {solve_part1(lines)}")
    print(f"2 -> {solve_part2(lines)}")


def solve_part1(lines: List[str]) -> int:
    almanac = parse_almanac(lines)
    return min(
        [calc_seed_dest(seed, almanac["almanac_maps"]) for seed in almanac["seeds"]]
    )


def solve_part2(lines: List[str]) -> int:
    almanac = parse_almanac_part2(lines)
    return min(
        source_range["start"]
        for source_range in chain.from_iterable(
            calc_seed_range_dest(seed_range, almanac["almanac_maps"])
            for seed_range in almanac["seed_ranges"]
        )
    )


def calc_seed_range_dest(
    seed_range: SourceRange, almanac_maps: List[AlmanacMap]
) -> List[SourceRange]:
    return reduce(
        lambda source_ranges, almanac_map: list(
            chain.from_iterable(
                calc_range_dest(source_range, almanac_map)
                for source_range in source_ranges
            )
        ),
        almanac_maps,
        [seed_range],
    )


def calc_range_dest(
    source_range: SourceRange, almanac_map: AlmanacMap
) -> List[SourceRange]:
    res: List[SourceRange] = list()

    for almanac_range in almanac_map:
        if source_range["start"] < almanac_range["source_start"]:
            subrange = SourceRange(
                start=source_range["start"],
                len=min(
                    almanac_range["source_start"] - source_range["start"],
                    source_range["len"],
                ),
            )
            res.append(subrange)

            source_range = SourceRange(
                start=source_range["start"] + subrange["len"],
                len=source_range["len"] - subrange["len"],
            )
            if source_range["len"] == 0:
                break

        if (
            source_range["start"] >= almanac_range["source_start"]
            and source_range["start"]
            < almanac_range["source_start"] + almanac_range["len"]
        ):
            subrange = SourceRange(
                start=almanac_range["dest_start"]
                + (source_range["start"] - almanac_range["source_start"]),
                len=min(
                    almanac_range["source_start"]
                    + almanac_range["len"]
                    - source_range["start"],
                    source_range["len"],
                ),
            )
            res.append(subrange)

            source_range = SourceRange(
                start=source_range["start"] + subrange["len"],
                len=source_range["len"] - subrange["len"],
            )
            if source_range["len"] == 0:
                break

    if source_range["len"] > 0:
        res.append(source_range)

    return res


def calc_seed_dest(seed: int, almanac_maps: List[AlmanacMap]) -> int:
    return reduce(calc_dest, almanac_maps, seed)


def calc_dest(source: int, almanac_map: AlmanacMap) -> int:
    range = find_almanac_range(source, almanac_map)
    if range is None:
        return source
    return range["dest_start"] + (source - range["source_start"])


def find_almanac_range(source: int, almanac_map: AlmanacMap) -> Optional[AlmanacRange]:
    ranges = [
        r
        for r in almanac_map
        if source in range(r["source_start"], r["source_start"] + r["len"])
    ]
    if len(ranges) == 1:
        return ranges[0]
    return None


def parse_almanac(lines: List[str]) -> Almanac:
    parts = split_list(lines, "")
    return Almanac(
        seeds=parse_seeds(parts[0][0]),
        almanac_maps=[parse_almanac_map(part) for part in parts[1:]],
    )


def parse_almanac_part2(lines: List[str]) -> AlmanacPart2:
    parts = split_list(lines, "")
    return AlmanacPart2(
        seed_ranges=parse_seed_ranges(parts[0][0]),
        almanac_maps=[parse_almanac_map(part) for part in parts[1:]],
    )


def parse_seeds(line: str) -> List[int]:
    return [int(part) for part in line.replace("seeds: ", "").split(" ")]


def parse_seed_ranges(line: str) -> List[SourceRange]:
    seed_parts = [int(part) for part in line.replace("seeds: ", "").split(" ")]
    return [
        SourceRange(start=batch[0], len=batch[1])
        for batch in split_to_chunks(seed_parts, 2)
    ]


def parse_almanac_map(lines: List[str]) -> AlmanacMap:
    return sorted(
        [
            AlmanacRange(
                dest_start=int(dest_start), source_start=int(source_start), len=int(len)
            )
            for dest_start, source_start, len in [line.split(" ") for line in lines[1:]]
        ],
        key=lambda r: r["source_start"],
    )


def split_list(list: List[str], separator: str) -> List[List[str]]:
    sep_idxs: List[int] = (
        [-1] + [idx for idx, s in enumerate(list) if s == separator] + [len(list)]
    )
    res: List[List[str]] = []
    for i in range(len(sep_idxs) - 1):
        res.append(list[sep_idxs[i] + 1 : sep_idxs[i + 1]])
    return res


T = TypeVar("T")


def split_to_chunks(list: List[T], chunk_size: int) -> List[List[T]]:
    return [list[i : i + chunk_size] for i in range(0, len(list), chunk_size)]


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
