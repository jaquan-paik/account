import hashlib

from caching.base import CachingQuerySet


class BaseCachingQuerySet(CachingQuerySet):
    pass


class UniqueCachingQuerySet(BaseCachingQuerySet):
    """
    cache machine에서 캐싱을 위해서 key를 만들때 db + sql 두가지를 사용해서 key를 만들게 되어 있어서
    database 수만큼 cache hit rate가 떨어지게 된다.
    따라서 key를 만드는 로직 안에서만 제한적으로 db를 read_1만 바로보게끔 한다.
    본 코드는 실제로 쿼리가 데이터베이스별로 분산되어 날아가는데 영향을 주지 않는다.
    """

    def query_key(self) -> str:
        return self._make_hash()

    def _make_hash(self) -> str:
        """
        self.model을 이용해서 고유한 값을 hash로 만듬
        모델 -> hash 변환과정에 멱등성을 충족함
        """
        return hashlib.md5(self.model.__class__.__name__.encode('utf-8')).hexdigest()
