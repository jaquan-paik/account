from typing import List

from apps.domains.account.models import User
from lib.base.repositories import BaseRepository


class UserRepository(BaseRepository):
    model_class = User

    @staticmethod
    def find_by_idxes(idxes: List[int]) -> List[User]:
        return User.objects.filter(idx__in=idxes)
