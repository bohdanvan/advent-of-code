from dataclasses import dataclass
from enum import IntEnum
from functools import reduce
from operator import mul
import re
from typing import Counter, List, Optional, Set, Tuple
import typing

BOARD_SIZE = (101, 103)
TEST_BOARD_SIZE = (11, 7)
TIME = 100

Pos = Tuple[int, int]


class Quadrant(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4


@dataclass
class Robot:
    pos: Pos
    velocity: Tuple[int, int]


def main() -> None:
    input = read_input("src/advent_of_code_2024/day14/input.txt")
    board_size = BOARD_SIZE

    print(f"1 -> {solve_part1(input, board_size)}")
    print(f"1 -> {solve_part2(input, board_size)}")


def solve_part1(input: List[str], board_size: Tuple[int, int]) -> int:
    robots = parse(input)

    quadrants = [
        quadrant
        for quadrant in [move_to_quadrant(robot, board_size, TIME) for robot in robots]
        if quadrant is not None
    ]
    return reduce(mul, Counter(quadrants).values())


def move_to_quadrant(
    robot: Robot, board_size: Tuple[int, int], time: int
) -> Optional[Quadrant]:
    # Returns quadrant
    new_robot = move_robot(robot, board_size, time)
    new_x, new_y = new_robot.pos

    size_x, size_y = board_size
    board_mid_x, board_mid_y = size_x // 2, size_y // 2

    if new_x > board_mid_x and new_y < board_mid_y:
        return Quadrant.ONE
    elif new_x < board_mid_x and new_y < board_mid_y:
        return Quadrant.TWO
    elif new_x < board_mid_x and new_y > board_mid_y:
        return Quadrant.THREE
    elif new_x > board_mid_x and new_y > board_mid_y:
        return Quadrant.FOUR
    else:
        return None


def move_robot(robot: Robot, board_size: Tuple[int, int], time: int) -> Robot:
    return Robot(
        pos=(
            move(robot.pos[0], robot.velocity[0], board_size[0], time),
            move(robot.pos[1], robot.velocity[1], board_size[1], time),
        ),
        velocity=robot.velocity,
    )


def move(pos: int, velocity: int, board_size: int, time: int) -> int:
    return (pos + time * velocity) % board_size


def solve_part2(input: List[str], board_size: Tuple[int, int]) -> int:
    robots = parse(input)

    out_file_name = "src/advent_of_code_2024/day14/out.txt"
    with open(out_file_name, "w") as file:
        for time in range(0, 10000):
            curr_robots = [move_robot(robot, board_size, time) for robot in robots]
            board_str = display_board(time, curr_robots, board_size)

            if "########" in board_str:
                file.write(board_str)
                return time

    return 0


def display_board(time: int, robots: List[Robot], board_size: Tuple[int, int]) -> str:
    robots_positions = {robot.pos for robot in robots}

    return (
        f"------ TIME: {time} ------\n"
        + "\n".join(
            "".join(
                "#" if (x, y) in robots_positions else " " for x in range(board_size[0])
            )
            for y in range(board_size[1])
        )
        + "\n\n"
    )


def parse(input: List[str]) -> List[Robot]:
    return list(map(parse_puzzle_input, input))


@typing.no_type_check
def parse_puzzle_input(line: str) -> Robot:
    groups = re.search(r"p=(.*) v=(.*)", line).groups()
    return Robot(
        pos=tuple(map(int, groups[0].strip().split(","))),
        velocity=tuple(map(int, groups[1].strip().split(","))),
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
