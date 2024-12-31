from typing import Callable, List, TypeVar

T = TypeVar("T")


def split_to_chunks(list: List[T], chunk_size: int) -> List[List[T]]:
    return [list[i : i + chunk_size] for i in range(0, len(list), chunk_size)]


def flatten(list: List[List[T]]) -> List[T]:
    return [item for sublist in list for item in sublist]


def create_array(size: int, filler: T) -> List[T]:
    return [filler for i in range(size)]


def create_matrix(rows: int, cols: int, filler: T) -> List[List[T]]:
    return [[filler for j in range(cols)] for i in range(rows)]


def create_3d_grid(
    x_size: int, y_size: int, z_size: int, filler: T
) -> List[List[List[T]]]:
    return [
        [[filler for k in range(z_size)] for j in range(y_size)] for i in range(x_size)
    ]


def deep_copy_matrix(matrix: List[List[T]]) -> List[List[T]]:
    return [row.copy() for row in matrix]


def split_list(list: List[T], separator: T) -> List[List[T]]:
    sep_idxs: List[int] = (
        [-1] + [idx for idx, s in enumerate(list) if s == separator] + [len(list)]
    )
    res: List[List[T]] = []
    for i in range(len(sep_idxs) - 1):
        res.append(list[sep_idxs[i] + 1 : sep_idxs[i + 1]])
    return res


def bin_search(a: List[T], verify_func: Callable[[T], bool]) -> T:
    lo = 0
    hi = len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if verify_func(a[mid]):
            hi = mid
        else:
            lo = mid + 1
    return a[lo]

# similar to bisect_left from bisect module
def bisect_left_lambda(a: List[T], lo=0, hi=None, verifier=None) -> int:
    if lo < 0:
        raise ValueError("lo must be non-negative")
    if hi is None:
        hi = len(a)

    while lo < hi:
        mid = (lo + hi) // 2
        if verifier(mid):
            lo = mid + 1
        else:
            hi = mid

    return lo
