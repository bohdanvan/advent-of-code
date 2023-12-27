from collections import deque
import queue
from typing import Dict, List, Set, Tuple
from pyvis.network import Network  # pip install pyvis


AdjDict = Dict[str, Set[str]]

# found with visualisation
DISCONNECTED_EDGES = [
    ("zqg", "mhb"),
    ("fjn", "mzb"),
    ("sjr", "jlt"),
]


def main() -> None:
    input = read_input("src/advent_of_code_2023/day25/input.txt")

    adj_dict = parse_adj_dict(input)
    # visualise_graph(adj_dict)

    print(f"1 -> {solve_part1(adj_dict, DISCONNECTED_EDGES)}")


def solve_part1(adj_dict: AdjDict, disconnected_adges: List[Tuple[str, str]]) -> int:
    for n1, n2 in disconnected_adges:
        adj_dict[n1].remove(n2)
        adj_dict[n2].remove(n1)

    return count_nodes(adj_dict, disconnected_adges[0][0]) * count_nodes(
        adj_dict, disconnected_adges[0][1]
    )


def count_nodes(adj_dict: AdjDict, start_node: str) -> int:
    visited: Set[str] = set()
    queue = deque([start_node])
    while len(queue) > 0:
        node = queue.pop()
        visited.add(node)
        queue.extend(
            [adj_node for adj_node in adj_dict[node] if adj_node not in visited]
        )

    return len(visited)


def visualise_graph(adj_dict: AdjDict):
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    for node in adj_dict.keys():
        net.add_node(node)

    for node, adj_nodes in adj_dict.items():
        for adj_node in adj_nodes:
            net.add_edge(node, adj_node)
    net.toggle_physics(True)
    net.show("mygraph.html", notebook=False)


def solve_part2():
    pass


def parse_adj_dict(lines: List[str]) -> AdjDict:
    adj_list = [parse_adj_node(line) for line in lines]

    adj_dict: AdjDict = {}
    for node, adj_nodes in adj_list:
        for adj_node in adj_nodes:
            add_adge(adj_dict, node, adj_node)
            add_adge(adj_dict, adj_node, node)

    return adj_dict


def add_adge(adj_dict: AdjDict, from_node: str, to_node: str):
    if from_node not in adj_dict:
        adj_dict[from_node] = set()
    adj_dict[from_node].add(to_node)


def parse_adj_node(s: str) -> Tuple[str, Set[str]]:
    parts = s.split(":")
    return (parts[0].strip(), set(parts[1].strip().split()))


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
