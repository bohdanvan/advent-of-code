from advent_of_code_2024.day7.day7 import (
    PART1_OPS_UNIVERSE,
    PART2_OPS_UNIVERSE,
    Operation,
    build_ops_permutations,
)


def test_build_ops_permutations():
    assert build_ops_permutations(2, PART1_OPS_UNIVERSE) == [
        [Operation.ADD, Operation.ADD],
        [Operation.ADD, Operation.MULT],
        [Operation.MULT, Operation.ADD],
        [Operation.MULT, Operation.MULT],
    ]

    assert build_ops_permutations(2, PART2_OPS_UNIVERSE) == [
        [Operation.ADD, Operation.ADD],
        [Operation.ADD, Operation.MULT],
        [Operation.ADD, Operation.CONCAT],
        [Operation.MULT, Operation.ADD],
        [Operation.MULT, Operation.MULT],
        [Operation.MULT, Operation.CONCAT],
        [Operation.CONCAT, Operation.ADD],
        [Operation.CONCAT, Operation.MULT],
        [Operation.CONCAT, Operation.CONCAT],
    ]
