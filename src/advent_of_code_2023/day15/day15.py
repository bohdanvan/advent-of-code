from collections import deque
import re
from typing import Deque, Dict, List, Optional, TypedDict


class BoxEntry(TypedDict):
    key: str
    value: int


class BoxHashMap:
    map: Dict[int, Deque[BoxEntry]] = dict()

    def put(self, key: str, value: int):
        hash = calc_hash(key)
        if hash not in self.map:
            self.map[hash] = deque()
        entry = self.__find_entry(key, hash)
        if entry is None:
            self.map[hash].append(BoxEntry(key=key, value=value))
        else:
            entry["value"] = value

    def __find_entry(self, key: str, hash: int) -> Optional[BoxEntry]:
        for entry in self.map[hash]:
            if key == entry["key"]:
                return entry
        return None

    def delete(self, key: str):
        hash = calc_hash(key)
        if hash not in self.map:
            return
        entry = self.__find_entry(key, hash)
        if entry is not None:
            self.map[hash].remove(entry)

    def get_total_score(self):
        return sum(
            sum(
                (hash + 1) * (idx + 1) * entry["value"] for idx, entry in enumerate(box)
            )
            for hash, box in self.map.items()
        )


class Input(TypedDict):
    label: str
    operation: str
    value: Optional[int]


def main() -> None:
    input = read_input("src/advent_of_code_2023/day15/input.txt")[0]

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(input: str) -> int:
    parts = [part for part in input.split(",")]
    print(f"len = {len(parts)}")
    return sum(calc_hash(part) for part in parts)


def calc_hash(s: str) -> int:
    res = 0
    for ch in s:
        res += ord(ch)
        res *= 17
        res %= 256
    return res


def solve_part2(input: str) -> int:
    parts = [parse(part) for part in input.split(",")]

    box_hash_map = BoxHashMap()
    for part in parts:
        if part["operation"] == "=" and part["value"] is not None:
            box_hash_map.put(part["label"], part["value"])
        else:
            box_hash_map.delete(part["label"])

    return box_hash_map.get_total_score()


def parse(s: str) -> Input:
    match = re.search(r"^([a-z]+)([\-\=])([1-9]*)$", s)
    if match is None:
        raise AssertionError(f"Match not found: {s}")
    if match.group(2) == "=":
        return Input(
            label=match.group(1), operation=match.group(2), value=int(match.group(3))
        )
    else:
        return Input(label=match.group(1), operation=match.group(2), value=None)


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
