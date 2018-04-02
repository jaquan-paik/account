
from caching.base import CachingQuerySet


class BaseCachingQuerySet(CachingQuerySet):
    """
    cache machine에서 캐싱을 위해서 key를 만들때 db + sql 두가지를 사용해서 key를 만들게 되어 있어서
    database 수만큼 cache hit rate가 떨어지게 된다.
    따라서 key를 만드는 로직 안에서만 제한적으로 db를 default만 바로보게 한다.
    본 코드는 실제로 쿼리가 데이터베이스별로 분산되어 날아가는데 영향을 주지 않는다.
    """

    def query_key(self):
        clone = self.query.clone()
        sql, params = clone.get_compiler(using='default').as_sql()
        return sql % params
