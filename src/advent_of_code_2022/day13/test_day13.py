from advent_of_code_2022.day13.day13 import compare, split_list

def test_split_list():
    assert split_list('[[1],[2,[3],4],5]') == ['[1]','[2,[3],4]','5']
    assert split_list(']1,[2,[3,[4,[5,6,7]]]],8,9]') == ['1','[2,[3,[4,[5,6,7]]]]','8','9']
    
def test_compare():
    assert compare('[1,1,3,1,1]', '[1,1,5,1,1]') < 0
    assert compare('[[4,4],4,4]', '[[4,4],4,4,4]') < 0
