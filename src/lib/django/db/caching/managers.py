from caching.base import CachingManager

from .constants import DEFAULT_CACHE_TTL
from .queryset import BaseCachingQuerySet, UniqueCachingQuerySet


class BaseCachingManager(CachingManager):
    CACHE_TTL = DEFAULT_CACHE_TTL
    MASTER_DATABASE = None

    def get_queryset(self):
        return BaseCachingQuerySet(self.model, using=self._db)

    def _get_queryset(self, no_cache: bool=False, is_fresh: bool=False):
        if is_fresh:
            return self.get_queryset().using(self._get_master_database())

        if no_cache:
            return self.no_cache()

        return self.cache(self.CACHE_TTL)

    def _get_master_database(self):
        if self.MASTER_DATABASE is None:
            raise NotImplementedError('MASTER_DATABASE를 설정하지 않았습니다.')

        return self.MASTER_DATABASE


class UniqueCachingManager(BaseCachingManager):
    def get_queryset(self):
        return UniqueCachingQuerySet(self.model, using=self._db)
