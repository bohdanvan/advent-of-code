from advent_of_code_2024.day4.day4 import to_asc_diagonals, to_desc_diagonals


def test_to_desc_diagonals():
    assert to_desc_diagonals(
        [
            "123",
            "456",
        ]
    ) == ["3", "26", "15", "4"]


def test_to_asc_diagonals():
    assert to_asc_diagonals(
        [
            "123",
            "456",
        ]
    ) == [
        "1",
        "42",
        "53",
        "6",
    ]
