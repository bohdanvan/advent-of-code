from advent_of_code_2024.day2.day2 import is_valid_report_part2


def test_is_valid_report_part2():
    assert is_valid_report_part2([1, 2, 3, 4, 5]) == True
    assert is_valid_report_part2([10, 2, 3, 4, 5]) == True
    assert is_valid_report_part2([1, 2, 3, 4, 50]) == True
    assert is_valid_report_part2([1, 20, 3, 4, 5]) == True
    assert is_valid_report_part2([1, 2, 30, 4, 5]) == True

    assert is_valid_report_part2(list(reversed([1, 2, 3, 4, 5]))) == True
    assert is_valid_report_part2(list(reversed([10, 2, 3, 4, 5]))) == True
    assert is_valid_report_part2(list(reversed([1, 2, 3, 4, 50]))) == True
    assert is_valid_report_part2(list(reversed([1, 20, 3, 4, 5]))) == True
    assert is_valid_report_part2(list(reversed([1, 2, 30, 4, 5]))) == True

    assert is_valid_report_part2([1, 20, 30, 4, 5]) == False
    assert is_valid_report_part2([1, 1, 1, 1, 1]) == False
