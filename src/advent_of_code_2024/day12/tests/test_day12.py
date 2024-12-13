from advent_of_code_2024.day12.day12 import count_sequences


def test_count_sequences():
    assert count_sequences([4, 5, 6, 8, 9, 20], {}) == 3
    assert count_sequences([4], {}) == 1
    assert count_sequences([4, 5, 6], {}) == 1

    assert count_sequences([4, 5, 6, 8, 9, 20], {5, 8}) == 4
    assert count_sequences([4, 5, 6], {5}) == 2
