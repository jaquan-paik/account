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
    def to_value(cls, string: str) -> int:
        for k, v in cls._STRING_MAP.items():
            if v == string:
                return k

        raise NotImplementedError

    @classmethod
    def get_string_map(cls) -> Dict:
        return cls._STRING_MAP

    @classmethod
    def to_key_from_string(cls, string: str) -> int:
        for k, v in cls._STRING_MAP.items():
            if v == string:
                return k

        raise NotImplementedError
