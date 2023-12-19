from collections import deque
from enum import Enum
from typing import List, TypedDict


class SpringType(Enum):
    OPERATIONAL = "."
    DAMAGED = "#"
    UNKNOWN = "?"


class SpringInput(TypedDict):
    field: List[SpringType]
    damaged_counts: List[int]


def main() -> None:
    input = read_input("src/advent_of_code_2023/day12/test.txt")
    spring_inputs = parse(input)

    # print(f"1 -> {solve_part1(spring_inputs)}")
    print(f"2 -> {solve_part2(spring_inputs)}")


def solve_part1(inputs: List[SpringInput]) -> int:
    arrangements = []
    for idx, input in enumerate(inputs):
        res = calc_arrangements(input["field"], input["damaged_counts"])
        print(f"{idx}: {res}")
        arrangements.append(res)
    # arrangements = [
    #     calc_arrangements(input["field"], input["damaged_counts"]) for input in inputs
    # ]
    print(arrangements)
    return sum(arrangements)


def solve_part2(inputs: List[SpringInput]) -> int:
    extended_input = [
        SpringInput(
            field=4 * (input["field"] + [SpringType.UNKNOWN]) + input["field"],
            damaged_counts=input["damaged_counts"] * 5,
        )
        for input in inputs
    ]
    return solve_part1(extended_input)


def calc_arrangements(field: List[SpringType], damaged_counts: List[int], idx=0) -> int:
    if idx >= len(field):
        is_valid = validate_field(field, damaged_counts)
        # print(f"{''.join([s.value for s in field])} -> {is_valid}")
        return 1 if is_valid else 0

    if field[idx] != SpringType.UNKNOWN:
        return calc_arrangements(field, damaged_counts, idx + 1)

    field[idx] = SpringType.OPERATIONAL
    operational_arrangements = calc_arrangements(field, damaged_counts, idx + 1)

    field[idx] = SpringType.DAMAGED
    damaged_arrangements = calc_arrangements(field, damaged_counts, idx + 1)

    field[idx] = SpringType.UNKNOWN  # restore

    return operational_arrangements + damaged_arrangements


def validate_field(field: List[SpringType], damaged_counts: List[int]) -> bool:
    damaged_counts_deque = deque(damaged_counts)

    curr_damaged_count = 1 if field[0] == SpringType.DAMAGED else 0
    for i in range(1, len(field)):
        if field[i] == SpringType.DAMAGED:
            curr_damaged_count += 1
        elif field[i - 1] == SpringType.DAMAGED:
            if (
                len(damaged_counts_deque) == 0
                or curr_damaged_count != damaged_counts_deque.popleft()
            ):
                return False
            curr_damaged_count = 0

    if (curr_damaged_count == 0 and len(damaged_counts_deque) > 0) or (
        curr_damaged_count > 0
        and (
            len(damaged_counts_deque) != 1
            or curr_damaged_count != damaged_counts_deque.popleft()
        )
    ):
        return False

    return True


def parse(lines: List[str]) -> List[SpringInput]:
    return [parse_line(line) for line in lines]


def parse_line(line: str) -> SpringInput:
    field_str, damaged_counts_str = line.split()
    return SpringInput(
        field=[SpringType(ch) for ch in field_str],
        damaged_counts=[int(part) for part in damaged_counts_str.split(",")],
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
