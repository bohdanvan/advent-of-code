from typing import List, TypeVar

T = TypeVar("T")


def split_to_chunks(list: List[T], chunk_size: int) -> List[List[T]]:
    return [list[i : i + chunk_size] for i in range(0, len(list), chunk_size)]
