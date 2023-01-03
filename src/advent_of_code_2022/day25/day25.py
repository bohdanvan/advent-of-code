from typing import Dict, List

SNAFU_DIGIT_TO_BASE_5: Dict[str, int] = {
    "0": 0,
    "1": 1,
    "2": 2,
    "=": 3,
    "-": 4,
}

SNAFU_DIGIT_TO_BASE_10: Dict[str, int] = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}


def main() -> None:
    input = read_input("src/advent_of_code_2022/day25/input.txt")

    print(f"1 -> {solve_part1(input)}")


def solve_part1(snafus: List[str]) -> str:
    decimals = [snafu_to_decimal(snafu) for snafu in snafus]
    decimal_sum = sum(decimals)
    return decimal_to_snafu(decimal_sum)


def snafu_to_decimal(snafu: str) -> int:
    res = 0
    mult = 1

    for snafu_d in reversed(snafu):
        d = SNAFU_DIGIT_TO_BASE_10[snafu_d]
        res += d * mult
        mult *= 5

    return res


def decimal_to_snafu(n: int) -> str:
    snafu_dec_digits = []
    rem = 0

    while n != 0:
        d = n % 5
        snafu_dec_digits.append(d)
        rem = 1 if d in (3, 4) else 0
        n = n // 5 + rem

    return "".join([base5_digit_to_snafu(int(d)) for d in reversed(snafu_dec_digits)])


def snafu_digit_to_base5(d: str) -> int:
    return SNAFU_DIGIT_TO_BASE_5[d]


def base10_digit_to_snafu(d: int) -> str:
    return list(SNAFU_DIGIT_TO_BASE_10.keys())[
        list(SNAFU_DIGIT_TO_BASE_10.values()).index(d)
    ]


def base5_digit_to_snafu(d: int) -> str:
    return list(SNAFU_DIGIT_TO_BASE_5.keys())[
        list(SNAFU_DIGIT_TO_BASE_5.values()).index(d)
    ]


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
