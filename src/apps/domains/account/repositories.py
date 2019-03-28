from typing import List

from apps.domains.account.models import User, UserModifiedHistory
from lib.base.repositories import BaseRepository


class UserModifiedHistoryRepository(BaseRepository):
    model_class = UserModifiedHistory

    @classmethod
    def get_last_ordered(cls) -> UserModifiedHistory:
        return cls.model_class.objects.filter(order___isnull=False).order_by('-order').first()

    @classmethod
    def find_unordered(cls, offset: int, limit: int) -> List[UserModifiedHistory]:
        return cls.model_class.objects.filter(order__isnull=True).order_by('id')[offset:offset + limit]

    @classmethod
    def find_after_order(cls, order: int, offset: int, limit: int) -> List[UserModifiedHistory]:
        return cls.model_class.objects.filter(order__gte=order).order_by('order')[offset:offset + limit]


class UserRepository(BaseRepository):
    model_class = User

    @classmethod
    def find_by_u_idxes(cls, u_idxes: List[int]) -> List[User]:
        return cls.model_class.objects.filter(idx__in=u_idxes)

    @classmethod
    def update(cls, entities: List, update_fields: List = None):
        super().update(entities)  # TODO user_modified_history 추가

    @classmethod
    def create(cls, entities: List, is_bulk: bool = False, bulk_bundle_count: int = 1000) -> List[User]:
        return super().create(entities, is_bulk, bulk_bundle_count)  # TODO user_modified_history 추가
