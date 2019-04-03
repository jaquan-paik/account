from typing import List

from apps.domains.account.models import User, UserModifiedHistory
from lib.base.repositories import BaseRepository


class UserModifiedHistoryRepository(BaseRepository):
    model_class = UserModifiedHistory

    @classmethod
    def get_last_ordered(cls) -> UserModifiedHistory:
        return cls.model_class.objects.filter(order__isnull=False).order_by('-order').first()

    @classmethod
    def find_unordered(cls, offset: int, limit: int) -> List[UserModifiedHistory]:
        return cls.model_class.objects.filter(order__isnull=True).order_by('id')[offset:offset + limit]

    @classmethod
    def find_order_or_over(cls, order: int, offset: int, limit: int) -> List[UserModifiedHistory]:
        return cls.model_class.objects.filter(order__gte=order).order_by('order')[offset:offset + limit]


class UserRepository(BaseRepository):
    model_class = User

    @classmethod
    def find_by_u_idxes(cls, u_idxes: List[int]) -> List[User]:
        return cls.model_class.objects.filter(idx__in=u_idxes)
