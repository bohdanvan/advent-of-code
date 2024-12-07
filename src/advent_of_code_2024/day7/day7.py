from enum import Enum
from functools import cache, reduce
from io import UnsupportedOperation
from typing import List, TypedDict


class Equation(TypedDict):
    result: int
    args: List[int]


class Operation(Enum):
    ADD = "+"
    MULT = "*"
    CONCAT = "||"


OPS_UNIVERSES = {
    "short_ops_universe": [
        Operation.ADD,
        Operation.MULT,
    ],
    "long_ops_universe": [
        Operation.ADD,
        Operation.MULT,
        Operation.CONCAT,
    ],
}


def main() -> None:
    input = read_input("src/advent_of_code_2024/day7/input.txt")
    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(input: List[str]) -> int:
    ## Bruite force solution: O(Lines * N * 2^N)
    equations = list(map(parse, input))
    return solve(equations, "short_ops_universe")


def solve_part2(input: List[str]) -> int:
    ## Bruite force solution: O(Lines * N * 3^N)
    equations = list(map(parse, input))
    return solve(equations, "long_ops_universe")


def solve(equations: List[Equation], ops_universe_name: str) -> int:
    return sum(
        map(
            lambda e: e["result"],
            filter(lambda eq: is_valid_equation(eq, ops_universe_name), equations),
        )
    )


DEBUG_COUNTER = 0


def is_valid_equation(equation: Equation, ops_universe_name: str) -> bool:
    global DEBUG_COUNTER
    DEBUG_COUNTER += 1
    print(f"{DEBUG_COUNTER} - len: {len(equation['args'])}")

    ops_list = build_ops_permutations_cached(
        len(equation["args"]) - 1, ops_universe_name
    )
    return any(
        map(
            lambda ops: eval_equation(equation["args"], ops) == equation["result"],
            ops_list,
        )
    )


@cache
def build_ops_permutations_cached(
    width: int, ops_universe_name: str
) -> List[List[Operation]]:
    ops_universe = OPS_UNIVERSES[ops_universe_name]

    return list(
        map(
            lambda bitmap: bitmap_to_ops(bitmap, width, ops_universe),
            range(len(ops_universe) ** width),
        )
    )


def bitmap_to_ops(
    bitmap: int, width: int, ops_universe: List[Operation]
) -> List[Operation]:
    return list(
        map(
            lambda digit: ops_universe[digit],
            to_digits(bitmap, len(ops_universe), width),
        )
    )


def to_digits(num: int, base: int, width: int) -> List[int]:
    digits: List[int] = []
    while num:
        digits.append(num % base)
        num //= base

    while len(digits) < width:
        digits.append(0)

    return list(reversed(digits))


def eval_equation(args: List[int], ops: List[Operation]) -> int:
    return reduce(lambda res, p: eval_op(res, p[0], p[1]), zip(args[1:], ops), args[0])


def eval_op(a: int, b: int, op: Operation) -> int:
    if op == Operation.ADD:
        return a + b
    elif op == Operation.MULT:
        return a * b
    elif op == Operation.CONCAT:
        return int(str(a) + str(b))
    else:
        raise AssertionError(f"unsupported operation: {op}")


def parse(line: str) -> Equation:
    tokens = line.split(":")
    return Equation(
        result=int(tokens[0].strip()), args=list(map(int, tokens[1].strip().split(" ")))
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
