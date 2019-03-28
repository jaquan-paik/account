from typing import List

from apps.domains.account.models import User
from lib.base.repositories import BaseRepository


class UserRepository(BaseRepository):
    model_class = User

    @classmethod
    def update(cls, users: List[User], update_fields: [] = None):
        # user_modified_history 추가
        super().update(users)

    @classmethod
    def create(cls, users: List[User], is_bulk: bool = False, bulk_bundle_count: int = 1000) -> List[User]:
        # user_modified_history 추가
        return super().create(users, is_bulk, bulk_bundle_count)

    @staticmethod
    def find_by_idxes(idxes: List[int]) -> List[User]:
        return User.objects.filter(idx__in=idxes)
