from collections import defaultdict, deque
from typing import Deque, Dict, List, TypedDict


class Block(TypedDict):
    id: int
    len: int
    pos: int


SPACE_BLOCK_ID = -1


def main() -> None:
    input = read_input("src/advent_of_code_2024/day9/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(input: str) -> int:
    # Runtime: O(len(input))
    blocks = parse_blocks(input)
    compacted_block = compact_blocks_part1(blocks)
    return checksum(compacted_block)


def solve_part2(input: str) -> int:
    # Runtime: O(len(input)^2)
    blocks = parse_blocks(input)
    compacted_block = compact_blocks_part2(blocks)
    return checksum(compacted_block)


def parse_blocks(input: str) -> List[Block]:
    res: List[Block] = []

    pos = 0
    id = 0
    is_block = True
    for len in map(int, input):
        if is_block:
            res.append(Block(id=id, len=len, pos=pos))
            id += 1

        pos += len
        is_block = not is_block

    return res


def compact_blocks_part1(blocks: List[Block]) -> List[Block]:
    res: List[Block] = []

    idx_left = 0
    idx_right = len(blocks) - 1

    right_block = blocks[idx_right]
    while idx_left < idx_right:
        left_block = blocks[idx_left]

        res.append(left_block)
        space = blocks[idx_left + 1]["pos"] - (left_block["pos"] + left_block["len"])

        while space != 0:
            if right_block["len"] <= space:
                res.append(
                    Block(
                        id=right_block["id"],
                        len=right_block["len"],
                        pos=res[-1]["pos"] + res[-1]["len"],
                    )
                )

                space -= right_block["len"]

                idx_right -= 1
                right_block = blocks[idx_right]
            else:  # right_block["len"] > space
                res.append(
                    Block(
                        id=right_block["id"],
                        len=space,
                        pos=res[-1]["pos"] + res[-1]["len"],
                    )
                )
                right_block = Block(
                    id=right_block["id"],
                    len=right_block["len"] - space,
                    pos=right_block["pos"],
                )
                space = 0

        idx_left += 1

    res.append(right_block)

    return res


def compact_blocks_part2(blocks: List[Block]) -> List[Block]:
    spaces: List[Block] = list(
        filter(
            lambda space: space["len"] > 0,
            map(
                lambda p: build_space_between_blocks(p[0], p[1]),
                zip(blocks[0:-1], blocks[1:]),
            ),
        )
    )

    res: List[Block] = []
    for block in reversed(blocks):
        for i in range(len(spaces)):
            space = spaces[i]
            if space["pos"] > block["pos"]:
                break

            if space["len"] >= block["len"]:
                res.append(Block(id=block["id"], len=block["len"], pos=space["pos"]))
                spaces[i] = Block(
                    id=SPACE_BLOCK_ID,
                    len=space["len"] - block["len"],
                    pos=space["pos"] + block["len"],
                )
                break

        if res and res[-1]["id"] != block["id"]:
            res.append(block)

    return res


def build_space_between_blocks(a: Block, b: Block) -> Block:
    return Block(
        id=SPACE_BLOCK_ID, len=b["pos"] - a["pos"] - a["len"], pos=a["pos"] + a["len"]
    )


def checksum(blocks: List[Block]) -> int:
    return sum(map(block_checksum, blocks))


def block_checksum(block: Block) -> int:
    # arithmetic progression
    pos_sum = block["len"] * (2 * block["pos"] + block["len"] - 1) // 2
    return block["id"] * pos_sum


def read_input(file_name: str) -> str:
    with open(file_name) as f:
        return f.readline().strip("\n")


if __name__ == "__main__":
    main()
