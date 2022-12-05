
from enum import Enum, IntEnum
from typing import List, Tuple

class Option(IntEnum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2
    

class RoundResult(Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"


def main() -> None:
    input = read_input('/Users/bvanchuhov/Projects/Python/algo-py/src/advent_of_code_2022/day2/input.txt')
    
    rounds_part1 = list(map(
        lambda r: (parse_opponent_option(r[0]), parse_my_option(r[1])), 
        input
    ))
    print(solve_part1(rounds_part1))
    
    rounds_part2 = list(map(
        lambda r: (parse_opponent_option(r[0]), parse_round_result(r[1])), 
        input
    ))
    print(solve_part2(rounds_part2))

    
def solve_part1(rounds: List[Tuple[Option, Option]]) -> int:
    return sum([win_score(r[0], r[1]) + choise_score(r[1]) for r in rounds])
     

def win_score(opponent_choice: Option, my_choice: Option) -> int:
    if opponent_choice == my_choice:
        return 3
    elif (int(my_choice) - int(opponent_choice)) in {1, -2}:
        return 6
    else:
        return 0


def choise_score(my_choice: Option) -> int:
    return int(my_choice) + 1
    

def solve_part2(rounds: List[Tuple[Option, RoundResult]]) -> int:
    return sum([win_score_by_result(r[1]) + choise_score(find_my_choise(r[0], r[1])) for r in rounds])


def win_score_by_result(result: RoundResult) -> int:
    if result == RoundResult.WIN:
        return 6
    elif result == RoundResult.DRAW:
        return 3
    else:
        return 0
    

def find_my_choise(opponent_choice: Option, result: RoundResult) -> Option:
    if result == RoundResult.DRAW:
        return opponent_choice
    elif result == RoundResult.WIN:
        return Option((int(opponent_choice) + 1) % 3)
    else:
        return Option((int(opponent_choice) - 1 + 3) % 3)


def parse_opponent_option(s: str) -> Option:
    if s == "A":
        return Option.ROCK
    elif s == "B":
        return Option.PAPER
    elif s == "C":
        return Option.SCISSORS
    raise AssertionError(f"Unsupported option: {s}")


def parse_my_option(s: str) -> Option:
    if s == "X":
        return Option.ROCK
    elif s == "Y":
        return Option.PAPER
    elif s == "Z":
        return Option.SCISSORS
    raise AssertionError(f"Unsupported option: {s}")


def parse_round_result(s: str) -> RoundResult:
    return RoundResult(s)


def read_input(file_name: str) -> List[List[str]]:
    with open(file_name) as f:
        return [line.split() for  line in f]
        

if __name__ == "__main__":
    main()
