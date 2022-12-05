from typing import List


def main() -> None:
    cals_per_elf = read_input('/Users/bvanchuhov/Projects/Python/algo-py/src/advent_of_code_2022/day1/input.txt')
    
    print(f"1 -> {most_calories(cals_per_elf)}")
    print(f"2 -> {total_top_calories(cals_per_elf, 3)}")
    
    
def most_calories(cals_per_elf: List[List[int]]) -> int:
    return max([sum(cals) for cals in cals_per_elf])


def total_top_calories(cals_per_elf: List[List[int]], top_count: int) -> int:
    cals = [sum(cals) for cals in cals_per_elf]
    cals.sort(reverse=True)
    return sum(cals[0:top_count])


def read_input(file_name: str) -> List[List[int]]:
    res: List[List[int]] = []
    with open(file_name) as f:
        curr_list: List[int] = []
        
        for line in f:
            if len(line.strip()) > 0:
                curr_list.append(int(line))
            else:
                res.append(curr_list)
                curr_list = []
    res.append(curr_list)           
    return res


if __name__ == "__main__":
    main()
