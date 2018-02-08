from typing import Dict, List


class BaseConstant:
    _LIST = []
    _STRING_MAP = {}

    @classmethod
    def get_list(cls) -> List:
        return cls._LIST

    @classmethod
    def get_choices(cls) -> List:
        return [(item, cls._STRING_MAP[item]) for item in cls._LIST]

    @classmethod
    def to_string(cls, item) -> str:
        return cls._STRING_MAP[item]

    @classmethod
    def get_string_map(cls) -> Dict:
        return cls._STRING_MAP
