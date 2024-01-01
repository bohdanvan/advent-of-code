import math
from typing import List, Optional, Sequence, Tuple, TypedDict

TEST_BOUNDARY: Sequence[int] = range(7, 27 + 1)
BOUNDARY: Sequence[int] = range(200000000000000, 400000000000000 + 1)

Point3d = Tuple[float, float, float]
Point2d = Tuple[float, float]


class Vec3d(TypedDict):
    pos: Point3d
    vel: Tuple[float, float, float]


class Vec2d(TypedDict):
    pos: Point2d
    vel: Tuple[float, float]


def main() -> None:
    input = read_input("src/advent_of_code_2023/day24/input.txt")
    vecs3d = parse_vecs3d(input)

    # print(
    #     find_intersection_2d(
    #         vec3d_to_vec2d(parse_vec3d("20, 25, 34 @ -2, -2, -4")),
    #         vec3d_to_vec2d(parse_vec3d("12, 31, 28 @ -1, -2, -1")),
    #     )
    # )

    print(f"1 -> {solve_part1(vecs3d, BOUNDARY)}")
    print(f"2 -> {solve_part2()}")


def solve_part1(vecs3d: List[Vec3d], boundary: Sequence[int]) -> int:
    vecs = [vec3d_to_vec2d(vec3d) for vec3d in vecs3d]
    vec_pairs = [
        (vecs[i], vecs[j]) for i in range(len(vecs)) for j in range(i + 1, len(vecs))
    ]
    return sum(
        1 if p is not None and is_within_boundaries_2d(p, boundary) else 0
        for p in [find_intersection_2d(v1, v2) for v1, v2 in vec_pairs]
    )


def solve_part2():
    pass


def is_within_boundaries_2d(p: Point2d, boundary: Sequence[int]) -> bool:
    return math.ceil(p[0]) in boundary and math.ceil(p[1]) in boundary


def vec3d_to_vec2d(vec3d: Vec3d) -> Vec2d:
    return Vec2d(
        pos=(vec3d["pos"][0], vec3d["pos"][1]),
        vel=(vec3d["vel"][0], vec3d["vel"][1]),
    )


def parse_vecs3d(lines: List[str]) -> List[Vec3d]:
    return [parse_vec3d(line) for line in lines]


# [t1, t2] = 1/(m_x_1 * -m_y_2 + m_x_2 * m_y_1) * [(b_x_1 - b_x_2), (b_y_1, b_y_2)]
def find_intersection_2d(v1: Vec2d, v2: Vec2d) -> Optional[Point2d]:
    denominator = v1["vel"][0] * (-v2["vel"][1]) + v2["vel"][0] * v1["vel"][1]
    if denominator == 0:
        return None
    t1 = (
        (v2["pos"][0] - v1["pos"][0]) * (-v2["vel"][1])
        + (v2["pos"][1] - v1["pos"][1]) * v2["vel"][0]
    ) / denominator
    t2 = (
        (v2["pos"][0] - v1["pos"][0]) * (-v1["vel"][1])
        + (v2["pos"][1] - v1["pos"][1]) * v1["vel"][0]
    ) / denominator
    if t1 < 0 or t2 < 0:
        return None

    return (v1["pos"][0] + t1 * v1["vel"][0], v1["pos"][1] + t1 * v1["vel"][1])


def parse_vec3d(s: str) -> Vec3d:
    parts = s.split("@")
    pos_parts = [int(part.strip()) for part in parts[0].split(",")]
    vel_parts = [int(part.strip()) for part in parts[1].split(",")]

    return Vec3d(
        pos=(pos_parts[0], pos_parts[1], pos_parts[2]),
        vel=(vel_parts[0], vel_parts[1], vel_parts[2]),
    )


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
