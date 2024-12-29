from collections import defaultdict
from itertools import combinations
from typing import Dict, List, Set, Tuple, cast

AdjDict = Dict[str, Set[str]]


def main() -> None:
    input = read_input("src/advent_of_code_2024/day23/input.txt")

    print(f"1 -> {solve_part1(input)}")
    print(f"2 -> {solve_part2(input)}")


def solve_part1(input: List[str]) -> int:
    edges = list(map(parse, input))
    adj = build_adj_list(edges)

    groups: Set[str] = set()
    for n1 in filter(lambda n: n.startswith("t"), adj.keys()):
        for n2 in adj[n1]:
            for n3 in adj[n1].intersection(adj[n2]):
                group = ",".join(sorted([n1, n2, n3]))
                groups.add(group)

    return len(groups)


def solve_part2(input: List[str]) -> str:
    edges = list(map(parse, input))
    adj = build_adj_list(edges)

    full_connected_clusters: List[List[str]] = []
    for n1 in adj.keys():
        for n2 in adj[n1]:
            shared_neighbors = adj[n1].intersection(adj[n2])

            cluster = [n1, n2] + list(shared_neighbors)
            if is_fully_connected(cluster, adj):
                full_connected_clusters.append(cluster)

    biggest_cluster = max(full_connected_clusters, key=len)
    return ",".join(sorted(biggest_cluster))


def is_fully_connected(cluster: List[str], adj: AdjDict) -> bool:
    return all(n2 in adj[n1] for n1, n2 in combinations(cluster, 2))


def build_adj_list(edges: List[Tuple[str, str]]) -> AdjDict:
    adj: AdjDict = defaultdict(set)
    for n1, n2 in edges:
        adj[n1].add(n2)
        adj[n2].add(n1)
    return adj


def parse(line: str) -> Tuple[str, str]:
    return cast(Tuple[str, str], tuple(line.split("-")))


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
