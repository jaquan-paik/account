from lib.base.constants import BaseConstant


class GenderType(BaseConstant):
    MALE = 0
    FEMALE = 1
    UNKNOWN = 2

    _LIST = (MALE, FEMALE)

    _STRING_MAP = {
        MALE: 'MALE',
        FEMALE: 'FEMALE',
        UNKNOWN: 'UNKNOWN'
    }

    _STORE_MAP = {
        'M': MALE,
        'F': FEMALE,
        '': UNKNOWN
    }

    @classmethod
    def to_value_from_store(cls, item):
        return cls._STORE_MAP[item]


class StatusType(BaseConstant):
    NORMAL = 0
    ABUSER = 1
    DORMANT = 2
    SECEDER = 3
    NEED_ACTIVATION = 4

    _LIST = (NORMAL, ABUSER, DORMANT, SECEDER, NEED_ACTIVATION)

    _STRING_MAP = {
        NORMAL: 'NORMAL',
        ABUSER: 'ABUSER',
        DORMANT: 'DORMANT',
        SECEDER: 'SECEDER',
        NEED_ACTIVATION: 'NEED_ACTIVATION'
    }
