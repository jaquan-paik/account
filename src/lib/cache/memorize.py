from typing import Callable


def memorize(func: Callable):
    _cache = {}

    def _decorator(*args, clear: bool=False, **kwargs):
        if clear:
            return func(*args, **kwargs)

        key = func.__name__ + str(args) + str(kwargs)
        if key not in _cache:
            _cache[key] = func(*args, **kwargs)
        return _cache[key]

    return _decorator
