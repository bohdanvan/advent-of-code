from typing import List, Set


def main() -> None:
    rucksacks = read_input(
        "/Users/bvanchuhov/Projects/Python/algo-py/src/advent_of_code_2022/day3/input.txt"
    )

    print(f"1 -> {solve_part1(rucksacks)}")
    print(f"2 -> {solve_part2(rucksacks)}")


def solve_part1(rucksacks: List[str]) -> int:
    return sum([find_rucksack_score(r) for r in rucksacks])


def find_rucksack_score(rucksack: str) -> int:
    length = len(rucksack)
    duplicates = find_duplicates(rucksack[0 : length // 2], rucksack[length // 2 :])
    return sum([item_score(item) for item in duplicates])


def find_duplicates(part1: str, part2: str) -> Set[str]:
    part1_chars = {ch for ch in part1}
    part2_chars = {ch for ch in part2}
    return part1_chars.intersection(part2_chars)


def solve_part2(rucksacks: List[str]) -> int:
    groups = split_to_chunks(rucksacks, 3)
    duplicates_per_group = [find_duplicates_list(g) for g in groups]
    all_duplicates = [
        item for duplicates in duplicates_per_group for item in duplicates
    ]
    return sum([item_score(item) for item in all_duplicates])


def find_duplicates_list(rucksacks: List[str]) -> Set[str]:
    res = {ch for ch in rucksacks[0]}
    for i in range(1, len(rucksacks)):
        res = res.intersection({ch for ch in rucksacks[i]})
    return res


def split_to_chunks(list: List[str], chunk_size: int) -> List[List[str]]:
    return [list[i : i + chunk_size] for i in range(0, len(list), chunk_size)]


def item_score(item: str) -> int:
    if item >= "a" and item <= "z":
        return ord(item) - ord("a") + 1
    elif item >= "A" and item <= "Z":
        return ord(item) - ord("A") + 27
    else:
        raise AssertionError(f"Invalid item: {item}")


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
