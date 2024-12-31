from advent_of_code_2024.day21.day21 import (
    DIRECTIONAL_KEYPAD,
    NUMERIC_KEYPAD,
    encode,
    encode_move,
)


# def test_encode_move():
#     assert encode_move("A", "5", NUMERIC_KEYPAD) == "<^^A"
#     assert encode_move("4", "3", NUMERIC_KEYPAD) == ">>vA"

#     assert encode_move("<", "A", DIRECTIONAL_KEYPAD) == ">>^A"
#     assert encode_move("A", "<", DIRECTIONAL_KEYPAD) == "v<<A"


MOVE_ORDERS = {NUMERIC_KEYPAD: "<^v>", DIRECTIONAL_KEYPAD: "<>^v"}


def test_encode():

    assert single_encode("029A") == "<A^A>^^AvvvA"
    assert double_encode("029A") == "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    assert len(triple_encode("029A")) == len(
        "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    )

    assert single_encode("980A") == "^^^A<AvvvA>A"
    assert double_encode("980A") == "<AAA>Av<<A>>^A<vAAA>^AvA^A"
    assert len(triple_encode("980A")) == len(
        "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A"
    )

    assert single_encode("179A") == "^<<A^^A>>AvvvA"
    assert double_encode("179A") == "<Av<AA>>^A<AA>AvAA^A<vAAA>^A"
    assert len(triple_encode("179A")) == len(
        "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
    )

    assert single_encode("456A") == "^^<<A>A>AvvA"
    assert double_encode("456A") == "<AAv<AA>>^AvA^AvA^A<vAA>^A"
    assert len(triple_encode("456A")) == len(
        "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"
    )

    assert single_encode("379A") == "^A<<^^A>>AvvvA"
    assert double_encode("379A") == "<A>Av<<AA>^AA>AvAA^A<vAAA>^A"
    assert len(triple_encode("379A")) == len(
        "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
    )


def single_encode(code: str):
    return encode(code, NUMERIC_KEYPAD)


def double_encode(code: str):
    return encode(single_encode(code), DIRECTIONAL_KEYPAD)


def triple_encode(code: str):
    return encode(double_encode(code), DIRECTIONAL_KEYPAD)
