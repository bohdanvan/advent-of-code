from enum import Enum
from typing import List, Optional, TypedDict

SCREEN_WIDTH = 40


class OperationType(Enum):
    ADDX = "addx"
    NOOP = "noop"


class Operation(TypedDict):
    type: OperationType
    val: Optional[int]


def main() -> None:
    input = read_input("src/advent_of_code_2022/day10/input.txt")
    ops = [parse_operation(line) for line in input]

    print(f"1 -> {solve_part1(ops)}")
    print(f"2 -> \n{solve_part2(ops)}")


def solve_part1(ops: List[Operation]) -> int:
    milestones = {x for x in range(20, 221, SCREEN_WIDTH)}

    res = 0
    register = 1
    step = 1

    for op in ops:
        if step in milestones:
            res += step * register

        if op["type"] == OperationType.ADDX:
            step += 1

            if step in milestones:
                res += step * register

            register = register + (op["val"] if op["val"] else 0)

        step += 1

    return res


def solve_part2(ops: List[Operation]):
    res: List[str] = []

    register = 1
    step = 0

    for op in ops:
        if (step % SCREEN_WIDTH) in {register - 1, register, register + 1}:
            res.append("#")
        else:
            res.append(".")

        if op["type"] == OperationType.ADDX:
            step += 1
            if (step % SCREEN_WIDTH) in {register - 1, register, register + 1}:
                res.append("#")
            else:
                res.append(".")

            register = register + (op["val"] if op["val"] else 0)

        step += 1

    print(f"step = {step}")

    return "\n".join(["".join(line) for line in split_to_chunks(res, SCREEN_WIDTH)])


def split_to_chunks(list: List[str], chunk_size: int) -> List[List[str]]:
    return [list[i : i + chunk_size] for i in range(0, len(list), chunk_size)]


def parse_operation(line: str) -> Operation:
    if line.startswith("addx "):
        return {
            "type": OperationType.ADDX,
            "val": int(line[len("addx ") :]),
        }
    else:
        return {
            "type": OperationType.NOOP,
            "val": None,
        }


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
