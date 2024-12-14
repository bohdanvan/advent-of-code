from dataclasses import dataclass
import re
from typing import List, Tuple
import typing
import numpy as np

from utils.utils import split_to_chunks


@dataclass
class GameInput:
    a: Tuple[int, int]
    b: Tuple[int, int]
    prize: Tuple[int, int]


PRICE_A = 3
PRICE_B = 1


def main() -> None:
    input = read_input("src/advent_of_code_2024/day13/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(input: List[str]) -> int:
    game_inputs = parse(input)
    return sum(map(solve_game, game_inputs))


def solve_part2(input: List[str]) -> int:
    game_inputs = list(map(increase_price, parse(input)))
    return sum(map(solve_game, game_inputs))


@typing.no_type_check
def increase_price(game_input: GameInput) -> GameInput:
    return GameInput(
        a=game_input.a,
        b=game_input.b,
        prize=tuple(map(lambda n: 10000000000000 + n, game_input.prize)),
    )


def solve_game(game_input: GameInput) -> int:
    ((ax, ay), (bx, by), (px, py)) = game_input.a, game_input.b, game_input.prize

    # steps_vec = buttons_matrix^(-1) * price_vec
    buttons_matrix = np.array(
        [
            [ax, bx],
            [ay, by],
        ]
    )
    price_vec = np.array([[px], [py]])

    steps_vec = np.linalg.inv(buttons_matrix).dot(price_vec)
    steps_a = round(float(steps_vec[0][0]))
    steps_b = round(float(steps_vec[1][0]))

    steps_int_vec = np.round(steps_vec).astype(np.int64)

    is_verified = np.array_equal(buttons_matrix.dot(steps_int_vec), price_vec)

    if is_verified:
        return PRICE_A * round(steps_a) + PRICE_B * round(steps_b)
    else:
        return 0


def parse(input: List[str]) -> List[GameInput]:
    return list(map(parse_game_input, split_to_chunks(input, 4)))


@typing.no_type_check
def parse_game_input(input: List[str]) -> GameInput:
    return GameInput(
        a=tuple(
            map(
                int,
                re.search(r"Button A: X\+(\d+), Y\+(\d+)", input[0]).groups(),
            ),
        ),
        b=tuple(
            map(
                int,
                re.search(r"Button B: X\+(\d+), Y\+(\d+)", input[1]).groups(),
            ),
        ),
        prize=tuple(
            map(
                int,
                re.search(r"Prize: X=(\d+), Y=(\d+)", input[2]).groups(),
            ),
        ),
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
