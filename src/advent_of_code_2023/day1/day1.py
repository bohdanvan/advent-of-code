from typing import List, Tuple

DIGIT_TO_STR = [
    (0, "0"),
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    (6, "6"),
    (7, "7"),
    (8, "8"),
    (9, "9"),
    (1, "one"),
    (2, "two"),
    (3, "three"),
    (4, "four"),
    (5, "five"),
    (6, "six"),
    (7, "seven"),
    (8, "eight"),
    (9, "nine"),
]


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line for line in f]


def first_digit(s: str) -> int:
    return min(
        list(
            filter(
                lambda p: p[1] >= 0,
                map(
                    lambda p: (p[0], s.find(p[1])),
                    DIGIT_TO_STR,
                ),
            )
        ),
        key=lambda p: p[1],
    )[0]


def last_digit(s: str) -> int:
    return max(
        list(
            filter(
                lambda p: p[1] >= 0,
                map(
                    lambda p: (p[0], s.rfind(p[1])),
                    DIGIT_TO_STR,
                ),
            )
        ),
        key=lambda p: p[1],
    )[0]


input = read_input("src/advent_of_code_2023/day1/input.txt")

sum = 0
for s in input:
    n = first_digit(s) * 10 + last_digit(s)
    sum += n
    print(n)

print(sum)
