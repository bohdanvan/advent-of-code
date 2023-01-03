from advent_of_code_2022.day25.day25 import decimal_to_snafu, snafu_to_decimal


def test_decimal_to_snafu():
    assert decimal_to_snafu(1) == "1"
    assert decimal_to_snafu(2) == "2"
    assert decimal_to_snafu(3) == "1="
    assert decimal_to_snafu(4) == "1-"
    assert decimal_to_snafu(5) == "10"
    assert decimal_to_snafu(6) == "11"
    assert decimal_to_snafu(7) == "12"
    assert decimal_to_snafu(8) == "2="
    assert decimal_to_snafu(2022) == "1=11-2"
    assert decimal_to_snafu(314159265) == "1121-1110-1=0"


def test_snafu_to_decimal():
    assert snafu_to_decimal("1=") == 3
    assert snafu_to_decimal("12") == 7
    assert snafu_to_decimal("1=-0-2") == 1747
    assert snafu_to_decimal("12111") == 906
    assert snafu_to_decimal("2=0=") == 198
    assert snafu_to_decimal("21") == 11
    assert snafu_to_decimal("2=01") == 201
    assert snafu_to_decimal("111") == 31
    assert snafu_to_decimal("20012") == 1257
    assert snafu_to_decimal("112") == 32
    assert snafu_to_decimal("1=-1=") == 353
    assert snafu_to_decimal("1-12") == 107
    assert snafu_to_decimal("122") == 37
