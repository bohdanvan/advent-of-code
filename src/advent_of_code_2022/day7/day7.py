from __future__ import annotations
import re
from typing import List


class Directory:
    # name: str
    # dirs: List[Directory] = []
    # files: List[File] = []
    # parent: Directory

    def __init__(self, name, parent=None):
        self.name = name
        self.dirs: List[Directory] = []
        self.files = []
        self.parent: Directory = parent
        self.size = None

    def __str__(self) -> str:
        return f"./{self.name}"


class File:
    # name: str
    # size: int

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __str__(self) -> str:
        return f"{self.name} ({self.size})"


def main() -> None:
    input = read_input(
        "src/advent_of_code_2022/day7/input.txt"
    )
    root_dir = parse_file_tree(input)
    dir_sizes = find_dir_size(root_dir)

    print(f"1 -> {solve_part1(dir_sizes)}")

    res_2 = solve_part2(dir_sizes=dir_sizes, used_space=root_dir.size,
                        total_disk_space=70000000, required_free_space=30000000)
    print(f"2 -> {res_2}")


def parse_file_tree(lines: List[str]):
    root_dir = Directory('/')

    curr_dir = root_dir

    for i in range(len(lines)):
        line = lines[i]
        if line.startswith('$ cd'):
            parsed = re.search(r'\$ cd (.*)', line)
            if not parsed:
                raise AssertionError
            path = parsed.group(1)
            if path == '/':
                pass
            elif path == '..':
                curr_dir = curr_dir.parent
            else:
                curr_dir = [
                    dir for dir in curr_dir.dirs if dir.name == path][0]
                
        elif line.startswith('$ ls'):
            pass
        
        elif line.startswith('dir'):
            parsed = re.search(r'dir (\w*)', line)
            if not parsed:
                raise AssertionError
            dir_name = parsed.group(1)

            new_dir = Directory(dir_name, curr_dir)
            curr_dir.dirs.append(new_dir)
            
        else:
            parsed = re.search(r'(\d+) ([\.\w]+)', line)
            if not parsed:
                raise AssertionError
            size, file_name = int(parsed.group(1)), parsed.group(2)

            new_file = File(file_name, size)
            curr_dir.files.append(new_file)

    return root_dir


def solve_part1(dir_sizes: List[int]) -> int:
    return sum([s for s in dir_sizes if s <= 100000])


def solve_part2(dir_sizes: List[int], used_space: int, total_disk_space: int, required_free_space: int) -> int:
    free_space = total_disk_space - used_space
    space_to_delete = required_free_space - free_space
    return min([s for s in dir_sizes if s >= space_to_delete])


def find_dir_size(root_dir: Directory) -> List[int]:
    dir_sizes: List[int] = []

    def find_size(dir: Directory):
        files_size = sum([file.size for file in dir.files])
        dirs_size = sum([find_size(dir) for dir in dir.dirs])
        total_size = files_size + dirs_size

        dir_sizes.append(total_size)
        dir.size = total_size

        return total_size

    find_size(root_dir)

    return dir_sizes


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
