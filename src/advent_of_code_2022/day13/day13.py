from functools import cmp_to_key
from typing import List, Tuple

from utils.utils import split_to_chunks


def main() -> None:
    input = read_input("src/advent_of_code_2022/day13/input.txt")

    signal_pairs = parse_pairs(input)
    print(f"1 -> {solve_part1(signal_pairs)}")

    signals = [line for line in input if line != ""]
    print(f"2 -> {solve_part2(signals)}")


def parse_pairs(input: List[str]) -> List[Tuple[str, str]]:
    return [(chunk[0], chunk[1]) for chunk in split_to_chunks(input, 3)]


def solve_part1(signal_pairs: List[Tuple[str, str]]):
    return sum([i + 1 for (i, (a, b)) in enumerate(signal_pairs) if compare(a, b) <= 0])


def solve_part2(signals: List[str]):
    signals.append("[[2]]")
    signals.append("[[6]]")

    signals.sort(key=cmp_to_key(lambda a, b: compare(a, b)))

    lower_idx = signals.index("[[2]]")
    higher_idx = signals.index("[[6]]")

    return (lower_idx + 1) * (higher_idx + 1)


def compare(a: str, b: str) -> int:
    if not is_list(a) and not is_list(b):
        return int(a) - int(b)

    if is_list(a) and is_list(b):
        list_a = split_list(a)
        list_b = split_list(b)

        for i in range(min(len(list_a), len(list_b))):
            cmp = compare(list_a[i], list_b[i])
            if cmp != 0:
                return cmp

        return len(list_a) - len(list_b)

    if is_list(a):
        return compare(a, f"[{b}]")
    else:
        return compare(f"[{a}]", b)


def is_list(s: str) -> bool:
    return s.startswith("[")


def split_list(s: str) -> List[str]:
    s = s[1:-1]
    if s == "":
        return []

    parts: List[str] = []
    tokens = s.split(",")

    i = 0
    while i < len(tokens):
        if tokens[i].startswith("["):
            bracket_count = tokens[i].count("[") - tokens[i].count("]")

            start_i = i

            i += 1
            while bracket_count != 0:
                bracket_count += tokens[i].count("[") - tokens[i].count("]")
                i += 1

            parts.append(",".join(tokens[start_i:i]))
        else:
            parts.append(tokens[i])
            i += 1

    return parts


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
