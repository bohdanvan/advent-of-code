import re
from typing import List, Optional, TypedDict


class Move(TypedDict):
    count: int
    from_idx: int
    to_idx: int


class CargoBoard(TypedDict):
    stacks: List[List[str]]
    moves: List[Move]


def main() -> None:
    input = read_input(
        "/Users/bvanchuhov/Projects/Python/algo-py/src/advent_of_code_2022/day5/input.txt"
    )

    print(f"1 -> {solve_part1(deep_copy(input['stacks']), input['moves'])}")
    print(f"2 -> {solve_part2(deep_copy(input['stacks']), input['moves'])}")


def deep_copy(matrix: List[List[str]]) -> List[List[str]]:
    return [row.copy() for row in matrix]
    
def solve_part1(stacks: List[List[str]], moves: List[Move]) -> str:
    for move in moves:
        from_idx = move["from_idx"]
        to_idx = move["to_idx"]
        count = move["count"]
        
        for i in range(count):
            stacks[to_idx].append(stacks[from_idx].pop())
    
    top_crates = [stack[-1] for stack in stacks]
    return ''.join(top_crates)


def solve_part2(stacks: List[List[str]], moves: List[Move]) -> str:
    for move in moves:
        from_idx = move["from_idx"]
        to_idx = move["to_idx"]
        count = move["count"]
        
        block = []
        for i in range(count):
            block.append(stacks[from_idx].pop())
            
        stacks[to_idx].extend(reversed(block))
    
    top_crates = [stack[-1] for stack in stacks]
    return ''.join(top_crates)



def read_input(file_name: str) -> CargoBoard:
    with open(file_name) as f:
        # rows, cols = tuple(map(int, re.search(r'(\d+) (\d+)', f.readline().strip()).groups(1, 2)))
        rows, cols = tuple(map(int, f.readline().strip().split()))

        matrix = [parse_line(f.readline()[:-1]) for i in range(rows)]
        stacks = matrix_to_stacks(matrix)
        
        f.readline() # skip
        f.readline() # skip

        moves = [parse_move(line.strip()) for line in f.readlines()]
        
        return {
            "stacks": stacks,
            "moves": moves
        }


def matrix_to_stacks(matrix: List[List[Optional[str]]]) -> List[List[str]]:
    stacks: List[List[str]] = []
    for j in range(len(matrix[0])):
        stack: List[str] = []
        for i in reversed(range(len(matrix))):
            val = matrix[i][j]
            if val:
                stack.append(val)
        stacks.append(stack)
    return stacks


def parse_line(s: str) -> List[Optional[str]]:
    crates = split_chunks(s + " ", 4)
    return [parse_crate(crate) for crate in crates]


def parse_crate(s: str) -> Optional[str]:
    m = re.search(r"\[(\w+)\] ", s)
    return m.group(1) if m else None


def parse_move(s: str) -> Move:
    m = re.search(r"move (\d+) from (\d+) to (\d+)", s)
    if not m:
        raise AssertionError
    return {
        "count": int(m.group(1)),
        "from_idx": int(m.group(2)) - 1,
        "to_idx": int(m.group(3)) - 1,
    }


def split_chunks(s: str, chunk_size: int) -> List[str]:
    return [s[i : i + chunk_size] for i in range(0, len(s), chunk_size)]


if __name__ == "__main__":
    main()
