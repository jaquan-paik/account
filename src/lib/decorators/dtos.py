from typing import Callable, List, Tuple


def as_dto(dto_class):
    def _decorator(func: Callable = None):
        def _wrapper(cls, *args, **kwargs):
            model = func(cls, *args, **kwargs)
            return dto_class(model)

        return _wrapper

    return _decorator


def as_dtos(dto_class):
    def _decorator(func: Callable = None):
        def _wrapper(cls, *args, **kwargs) -> List:
            models = func(cls, *args, **kwargs)
            return [dto_class(model) for model in models]

        return _wrapper

    return _decorator


def as_dtos_from_tuple(dto_class):
    def _decorator(func: Callable = None):
        def _wrapper(cls, *args, **kwargs) -> Tuple:
            models, extra = func(cls, *args, **kwargs)
            return [dto_class(model) for model in models], extra

        return _wrapper

    return _decorator
