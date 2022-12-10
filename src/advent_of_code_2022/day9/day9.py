from enum import Enum
from typing import List, Set, Tuple, TypedDict


class Direction(Enum):
    RIGHT = "R"
    LEFT = "L"
    UP = "U"
    DOWN = "D"


class Move(TypedDict):
    direction: Direction
    steps: int


Pos = Tuple[int, int]


def main() -> None:
    input = read_input("src/advent_of_code_2022/day9/input.txt")
    moves = [parse_line(line) for line in input]

    print(f"1 -> {solve_part1(moves)}")
    print(f"2 -> {solve_part2(moves)}")


def parse_line(line: str) -> Move:
    split = line.split()
    return {"direction": Direction(split[0]), "steps": int(split[1])}


def solve_part1(moves: List[Move]):
    visited: Set[Pos] = set({})

    head_pos = (0, 0)
    tail_pos = (0, 0)

    visited.add(tail_pos)

    for move in moves:
        for step in range(move["steps"]):
            new_head_pos = step_move(head_pos, move["direction"])
            new_tail_pos = find_new_tail_pos(new_head_pos, tail_pos)

            visited.add(new_tail_pos)

            head_pos = new_head_pos
            tail_pos = new_tail_pos

    return len(visited)


def solve_part2(moves: List[Move]):
    visited: Set[Pos] = set({})

    rope = [(0, 0) for _ in range(10)]
    # print_rope(rope)

    visited.add(rope[-1])

    for move in moves:
        for step in range(move["steps"]):
            rope[0] = step_move(rope[0], move["direction"])
            for i in range(1, len(rope)):
                rope[i] = find_new_tail_pos(
                    new_head_pos=rope[i - 1],
                    tail_pos=rope[i],
                )

            visited.add(rope[-1])

            # print(f"{move}, step = {step}")
            # print_rope(rope)

    return len(visited)


def print_rope(rope: List[Pos]) -> None:
    shift_x = shift_y = 30
    size = shift_x * 2
    matrix: List[List[str]] = [["-" for _ in range(size)] for _ in range(size)]
    for i in range(len(rope)):
        pos = rope[i]
        if matrix[pos[0] + shift_x][pos[1] + shift_y] == "-":
            matrix[pos[0] + shift_x][pos[1] + shift_y] = str(i)

    for row in reversed(matrix):
        print(" ".join(row))

    print("----")


def step_move(pos: Pos, direction: Direction) -> Pos:
    if direction == Direction.RIGHT:
        return (pos[0], pos[1] + 1)
    elif direction == Direction.LEFT:
        return (pos[0], pos[1] - 1)
    elif direction == Direction.UP:
        return (pos[0] + 1, pos[1])
    elif direction == Direction.DOWN:
        return (pos[0] - 1, pos[1])
    else:
        raise AssertionError()


def find_new_tail_pos(new_head_pos: Pos, tail_pos: Pos) -> Pos:
    delta_x = new_head_pos[0] - tail_pos[0]
    delta_y = new_head_pos[1] - tail_pos[1]

    distance = max(abs(delta_x), abs(delta_y))
    if distance <= 1:
        return tail_pos

    return (tail_pos[0] + inc_div(delta_x), tail_pos[1] + inc_div(delta_y))

    # if (abs(delta_x) == 2):
    #     return (tail_pos[0] + (delta_x // 2), new_head_pos[1])

    # if (abs(delta_y) == 2):
    #     return (new_head_pos[0], tail_pos[1] + (delta_y // 2))

    # if delta_x == 0 or delta_y == 0:
    #     old_head_pos

    # return old_head_pos

    # if distance == 1:
    #     return old_head_pos

    # delta_x = new_head_pos[0] - old_head_pos[0]
    # delta_y = new_head_pos[1] - old_head_pos[1]

    # return (tail_pos[0] + (delta_x, tail_pos[1] + delta_y)


def inc_div(x: int) -> int:
    return (x + 1) // 2 if x >= 0 else -((-x + 1) // 2)


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
