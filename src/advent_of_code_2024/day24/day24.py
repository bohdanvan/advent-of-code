from collections import deque
from dataclasses import dataclass
import re
from typing import Dict, List, Tuple, cast
import typing

from utils.utils import split_list


@dataclass
class Gate:
    input_keys: Tuple[str, str]
    operator: str
    output_key: str

    def __init__(self, input_keys: Tuple[str, str], operator: str, output_key: str):
        self.input_keys = cast(Tuple[str, str], tuple(sorted(input_keys)))
        self.operator = operator
        self.output_key = output_key

    def exec(self, left_input: int, right_input: int) -> int:
        if self.operator == "AND":
            return left_input & right_input
        elif self.operator == "OR":
            return left_input | right_input
        elif self.operator == "XOR":
            return left_input ^ right_input
        else:
            raise AssertionError(f"unsupported operator: {self.operator}")

    @typing.no_type_check
    def build_output_name(self, left_input_name: str, right_input_name: str) -> str:
        if len(left_input_name) == 3 and len(right_input_name) == 3:
            (left_input_name, right_input_name) = tuple(
                sorted(
                    [left_input_name, right_input_name],
                ),
            )
        else:
            (left_input_name, right_input_name) = tuple(
                sorted(
                    sorted(
                        [left_input_name, right_input_name],
                        reverse=True,
                    ),
                    key=len,
                )
            )

        if len(left_input_name) > 3:
            left_input_name = f"({left_input_name})"
        if len(right_input_name) > 3:
            right_input_name = f"({right_input_name})"
        return f"{left_input_name} {self.operator} {right_input_name}"


@dataclass
class PuzzleInput:
    inputs: Dict[str, int]
    gates: List[Gate]


def main() -> None:
    lines = read_input("src/advent_of_code_2024/day24/input.txt")

    print(f"1 -> {solve_part1(lines)}")

    analyse_part2(lines)
    print(f"2 -> {solve_part2(lines)}")


def solve_part1(lines: List[str]) -> int:
    puzzle_inptut = parse(lines)

    inputs = dict(puzzle_inptut.inputs)
    gates = deque(puzzle_inptut.gates)

    while gates:
        gate = gates.popleft()
        (left_input_key, right_input_key) = gate.input_keys
        (left_input, right_input) = (
            inputs.get(left_input_key, None),
            inputs.get(right_input_key, None),
        )
        if left_input is not None and right_input is not None:
            output = gate.exec(left_input, right_input)
            inputs[gate.output_key] = output
        else:
            gates.append(gate)

    res_str = "".join(
        str(val)
        for _, val in sorted(
            [
                (int(input_key.replace("z", "")), val)
                for input_key, val in inputs.items()
                if input_key.startswith("z")
            ],
            key=lambda p: p[0],
            reverse=True,
        )
    )
    res = int(res_str, 2)

    return res


def analyse_part2(lines: List[str]):
    puzzle_inptut = parse(lines)

    gates = puzzle_inptut.gates
    gates = swap_gates(
        puzzle_inptut.gates,
        [("z19", "sbg"), ("z37", "dsd"), ("z12", "djg"), ("mcq", "hjm")],
    )

    gates_queue = deque(gates)
    input_keys = set(puzzle_inptut.inputs.keys())

    output_names = {input: input for input in input_keys}

    while gates_queue:
        gate = gates_queue.popleft()
        (left_input_key, right_input_key) = gate.input_keys
        if left_input_key in input_keys and right_input_key in input_keys:
            output_name = gate.build_output_name(
                output_names[left_input_key], output_names[right_input_key]
            )
            output_names[gate.output_key] = output_name
            input_keys.add(gate.output_key)
        else:
            gates_queue.append(gate)

    z_output_names = list(
        sorted(
            ((key, name) for key, name in output_names.items() if key.startswith("z")),
            key=lambda p: p[0],
        )
    )

    for key, name in z_output_names:
        print(f"{key} -> {name}")
        print()


def solve_part2(lines: List[str]) -> str:
    return ",".join(sorted(["z19", "sbg", "z37", "dsd", "z12", "djg", "mcq", "hjm"]))


def swap_gates(gates: List[Gate], swap_keys_list: List[Tuple[str, str]]) -> List[Gate]:
    swapped_gates: List[Gate] = []
    for gate in gates:
        swapped_gate = gate
        for swap_keys in swap_keys_list:
            if gate.output_key == swap_keys[0]:
                swapped_gate = Gate(gate.input_keys, gate.operator, swap_keys[1])
            elif gate.output_key == swap_keys[1]:
                swapped_gate = Gate(gate.input_keys, gate.operator, swap_keys[0])

        swapped_gates.append(swapped_gate)
    return swapped_gates


def parse(lines: List[str]) -> PuzzleInput:
    parts = split_list(lines, "")

    return PuzzleInput(
        inputs={
            line.split(":")[0].strip(): int(line.split(":")[1].strip())
            for line in parts[0]
        },
        gates=[parse_gate(line) for line in parts[1]],
    )


def parse_gate(line: str) -> Gate:
    match = re.search("^(.*) (\w*) (.*) -> (.*)$", line.strip())
    if not match:
        raise AssertionError()
    return Gate(
        input_keys=(match.group(1), match.group(3)),
        output_key=match.group(4),
        operator=match.group(2),
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
