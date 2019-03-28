from typing import List

from apps.domains.account.models import User
from lib.base.repositories import BaseRepository


class UserRepository(BaseRepository):
    model_class = User

    @classmethod
    def update(cls, users: List[User], update_fields: [] = None):
        super().update(users)  # TODO user_modified_history 추가

    @classmethod
    def create(cls, users: List[User], is_bulk: bool = False, bulk_bundle_count: int = 1000) -> List[User]:
        return super().create(users, is_bulk, bulk_bundle_count)  # TODO user_modified_history 추가

    @staticmethod
    def find_by_idxes(idxes: List[int]) -> List[User]:
        return User.objects.filter(idx__in=idxes)
