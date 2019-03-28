from typing import List

from apps.domains.account.models import UserModifiedHistory
from lib.base.repositories import BaseRepository


class UserModifiedHistoryRepository(BaseRepository):
    model_class = UserModifiedHistory

    @classmethod
    def get_last_ordered(cls) -> UserModifiedHistory:
        return cls.model_class.objects.filter(order___isnull=False).order_by('-order').first()

    @classmethod
    def find_unordered(cls, offset: int, limit: int) -> List[UserModifiedHistory]:
        return cls.model_class.objects.filter(order__isnull=True).order_by('id')[offset:offset + limit]
