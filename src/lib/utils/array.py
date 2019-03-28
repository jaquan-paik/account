import itertools
from typing import Callable, Dict, List


def to_dict(items: List, key: str = None, func: Callable = None) -> Dict:
    if key is None and func is None:
        raise NotImplementedError
    if key is not None:
        return dict((getattr(item, key), item) for item in items)

    return dict((func(item), item) for item in items)


def to_list_dict(items: List, key: str = None, func: Callable = None) -> Dict:
    if key is None and func is None:
        raise NotImplementedError

    result = {}
    for item in items:
        item_key = func(item) if key is None else getattr(item, key)
        if item_key not in result:
            result[item_key] = []

        result[item_key].append(item)

    return result


def be_unique(items: List, key: str = None, func: Callable = None):
    return list(to_dict(items, key=key, func=func).values())


def chunk(l: List, n: int) -> List[List]:
    return [l[i:i + n] for i in range(0, len(l), n)]


def chunk_for_iter(l: List, n: int) -> List[List]:
    it = iter(l)
    while True:
        temp_chunk = tuple(itertools.islice(it, n))
        if not temp_chunk:
            return
        yield temp_chunk
