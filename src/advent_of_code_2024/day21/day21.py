from functools import cache
from itertools import permutations, product
from typing import Dict, List, Tuple


Pos = Tuple[int, int]


class Keypad:
    board: List[str]
    pos_map: Dict[str, Pos]

    def __init__(self, board: List[str]):
        self.board = board
        self.pos_map = self._build_pos_map()

    def get_button_pos(self, button: str) -> Pos:
        return self.pos_map[button]

    def get(self, pos: Pos) -> str:
        return self.board[pos[0]][pos[1]]

    def _build_pos_map(self) -> Dict[str, Pos]:
        return {
            self.board[i][j]: (i, j)
            for i in range(len(self.board))
            for j in range(len(self.board[i]))
            if self.board[i][j] != " "
        }


NUMERIC_KEYPAD = Keypad(
    [
        "789",
        "456",
        "123",
        " 0A",
    ]
)
DIRECTIONAL_KEYPAD = Keypad(
    [
        " ^A",
        "<v>",
    ]
)

MOVE_POSITION_INC: Dict[str, Tuple[int, int]] = {
    "<": (0, -1),
    ">": (0, +1),
    "^": (-1, 0),
    "v": (1, 0),
}


def main() -> None:
    input = read_input("src/advent_of_code_2024/day21/input.txt")

    print(f"1 -> {solve_part1(input)}")
    # print(f"2 -> {solve_part2(input)}")

    # multi_encode("539A", {
    #     NUMERIC_KEYPAD: "<^v>",
    #     DIRECTIONAL_KEYPAD: "<>^v"
    # })

    # multi_encode("37")
    # multi_decode("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A")

    # multi_encode("029A")
    # multi_decode("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")

    # multi_encode("980A")
    # multi_decode("<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A")

    # multi_encode("179A")
    # multi_decode("<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")

    # multi_encode("456A")
    # multi_decode("<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A")

    # multi_encode("379A")
    # multi_decode("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")


def solve_part1(codes: List[str]) -> int:
    return sum(build_code_complexity(code, 2) for code in codes)


def solve_part2(codes: List[str]) -> int:
    return sum(build_code_complexity(code, 25) for code in codes)


def build_code_complexity(code: str, keypads_count: int) -> int:
    num_code = int(code.replace("A", ""))
    multi_encoded_len = multi_encode_len(code, keypads_count)
    # print(f"### code '{code}': {len(multi_encoded)} * {num_code}")
    # print()
    return multi_encoded_len * num_code


def multi_encode_len(code: str, keypads_count: int) -> int:
    code = encode(code, NUMERIC_KEYPAD)
    return multi_encode_directional_len(code, keypads_count)


@cache
def multi_encode_directional_len(code: str, keypads_count: int) -> int:
    if keypads_count == 0:
        return len(code)

    start_btn = "A"
    res_len = 0
    for finish_btn in code:
        directional_code = encode_move(start_btn, finish_btn, DIRECTIONAL_KEYPAD)
        res_len += multi_encode_directional_len(directional_code, keypads_count - 1)
        start_btn = finish_btn

    print(f"Code: {code} (keypads_count = {keypads_count}, res_len = {res_len})")

    return res_len


# def multi_encode(code: str, keypads_count: int) -> str:
#     # robot1_code = encode(code, NUMERIC_KEYPAD, move_orders)
#     # robot2_code = encode(robot1_code, DIRECTIONAL_KEYPAD, move_orders)
#     # robot3_code = encode(robot2_code, DIRECTIONAL_KEYPAD, move_orders)

#     code = encode(code, NUMERIC_KEYPAD)
#     for idx in range(keypads_count):
#         code = encode(code, DIRECTIONAL_KEYPAD, idx)

#     # print(f"Encode: {code}")
#     # print(f"code: {code}")
#     # print(f"robot 1: {robot1_code}")
#     # print(f"robot 2: {robot2_code}")
#     # print(f"robot 3: {robot3_code}")

#     return code

# def best_multi_encode(code: str) -> str:
#     all_move_orders = build_move_orders()

#     results = [
#         (
#             f"{move_orders[NUMERIC_KEYPAD]} / {move_orders[DIRECTIONAL_KEYPAD]}",
#             multi_encode(code, move_orders),
#         )
#         for move_orders in all_move_orders
#     ]

#     min_res = min(results, key=lambda p: len(p[1]))

#     print(f"best move_orders for '{code}': {min_res[0]}")

#     return min_res[1]


# def build_move_orders() -> List[Dict[Keypad, str]]:
#     move_orders_1 = ["".join(p) for p in permutations("<>^v")]
#     move_orders_2 = ["".join(p) for p in permutations("<>^v")]
#     list()
#     return [
#         {NUMERIC_KEYPAD: mo1, DIRECTIONAL_KEYPAD: mo2}
#         for (mo1, mo2) in product(move_orders_1, move_orders_2)
#     ]

# @cache
# def encode_directional_move_len(start_btn: str, finish_btn: str, idx: int, max_idx: int) -> int:
#     start_btn = "A"
#     res_len = 0
#     for finish_btn in code:
#         btn_code = finish_btn
#         direction_code = encode_move(start_btn, finish_btn, DIRECTIONAL_KEYPAD)
#         res_len +=
#         start_btn = finish_btn


def multi_decode(robot3_code: str) -> str:
    robot2_code = decode(robot3_code, DIRECTIONAL_KEYPAD)
    robot1_code = decode(robot2_code, DIRECTIONAL_KEYPAD)
    code = decode(robot1_code, NUMERIC_KEYPAD)

    print(f"Decode: {code}")
    print(f"code: {code}")
    print(f"robot 1: {robot1_code}")
    print(f"robot 2: {robot2_code}")
    print(f"robot 3: {robot3_code}")

    return code


def encode(code: str, keypad: Keypad) -> str:
    start_btn = "A"

    direction_code = ""
    for finish_btn in code:
        direction_code += encode_move(start_btn, finish_btn, keypad)
        start_btn = finish_btn

    return direction_code


def encode_move(start_btn: str, finish_btn: str, keypad: Keypad) -> str:
    start_pos = keypad.get_button_pos(start_btn)
    finish_pos = keypad.get_button_pos(finish_btn)

    direction_code = ""
    if start_pos[1] < finish_pos[1]:
        direction_code += ">" * (finish_pos[1] - start_pos[1])
    if start_pos[0] > finish_pos[0]:
        direction_code += "^" * (start_pos[0] - finish_pos[0])
    if start_pos[1] > finish_pos[1]:
        direction_code += "<" * (start_pos[1] - finish_pos[1])
    if start_pos[0] < finish_pos[0]:
        direction_code += "v" * (finish_pos[0] - start_pos[0])

    if keypad == NUMERIC_KEYPAD:
        if start_btn in {"A", "0"} and finish_btn in {"1", "4", "7"}:
            direction_code = sort_by_order(direction_code, "^<>v")
        elif start_btn in {"1", "4", "7"} and finish_btn in {"A", "0"}:
            direction_code = sort_by_order(direction_code, "><^v")
        else:
            direction_code = sort_by_order(direction_code, "<>^v")
    else:
        if finish_btn == "<":
            direction_code = sort_by_order(direction_code, "v<>^")
        elif start_btn == "<":
            direction_code = sort_by_order(direction_code, "><^v")
        else:
            direction_code = sort_by_order(direction_code, "<>^v")

    direction_code += "A"

    return direction_code


def sort_by_order(s: str, sort_order: str) -> str:
    order_map = {sort_order[i]: i for i in range(len(sort_order))}
    return "".join(sorted((ch for ch in s), key=lambda e: order_map[e]))


def decode(code: str, keypad: Keypad) -> str:
    pos = keypad.get_button_pos("A")

    res = ""
    for move in code:
        if move == "A":
            res += keypad.get(pos)
        else:
            pos = decode_move(pos, move)
    return res


def decode_move(pos: Pos, move: str) -> Pos:
    pos_inc = MOVE_POSITION_INC[move]
    return (pos[0] + pos_inc[0], pos[1] + pos_inc[1])


def read_input(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    main()
