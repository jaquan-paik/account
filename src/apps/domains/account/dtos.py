from datetime import datetime
from typing import Dict, Optional

from apps.domains.account.constants import StatusType, GenderType
from lib.utils.date import strptime
from lib.utils.format import DateTimeFormat


class UserDto:
    __slots__ = ['_user', ]

    def __init__(self, user: Dict):
        self._user = user

    @property
    def u_id(self) -> int:
        return self._user['u_id']

    @property
    def u_idx(self) -> str:
        return self._user['u_idx']

    @property
    def name(self) -> str:
        return self._user['name']

    @property
    def reg_date(self) -> datetime:
        return strptime(self._user['reg_date'], DateTimeFormat.ISO_YMD_HMSZ)

    @property
    def ip(self) -> str:
        return self._user['ip']

    @property
    def device_id(self) -> str:
        return self._user['device_id']

    @property
    def email(self) -> str:
        return self._user['email']

    @property
    def birth_date(self) -> Optional[datetime]:
        return None if not self._user['birth_date'] else strptime(self._user['birth_date'], DateTimeFormat.ISO_YMD_HMSZ)

    @property
    def gender(self) -> int:
        return GenderType.to_value_from_store(self._user['gender'])

    @property
    def verified(self) -> bool:
        return self._user['verified']

    @property
    def status(self) -> int:
        return StatusType.to_key_from_string(self._user['status'])

    @property
    def email_verify_date(self) -> Optional[datetime]:
        return None if not self._user['email_verify_date'] else strptime(self._user['email_verify_date'], DateTimeFormat.ISO_YMD_HMSZ)

    @property
    def updated_at(self) -> Optional[datetime]:
        return None if not self._user['updated_at'] else strptime(self._user['updated_at'], DateTimeFormat.ISO_YMD_HMSZ)
