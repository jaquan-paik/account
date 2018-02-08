import typing

from redis import Redis

from .config import RedisConfig


class RedisManager:
    """
    :type database: int
    """
    database = None

    def get_connection(self):
        if self.database is None:
            raise AttributeError('database is None')

        return Redis(host=RedisConfig.get_host(), port=RedisConfig.get_port(), db=self.database)

    def rpush_expire(self, key: typing.Any, value: typing.Any, expire: int) -> None:
        conn = self.get_connection()
        conn.rpush(key, value)
        conn.expire(key, expire)

    def get_multi_list(self, match: str, count: int):
        conn = self.get_connection()

        _, keys = conn.scan(cursor=0, match=match, count=count)

        pipeline = conn.pipeline()
        for key in keys:
            pipeline.lrange(key, 0, -1)
        two_dimensional_items = pipeline.execute()
        flattened_items = sum(two_dimensional_items, [])

        return flattened_items

    def set_nx_ex(self, key: str, value: str, ttl: int) -> bool:
        conn = self.get_connection()
        return conn.set(key, value, ex=ttl, nx=True)

    def delete(self, key: str):
        conn = self.get_connection()
        return conn.delete(key)

    def expire(self, key: str, ttl: int):
        conn = self.get_connection()
        return conn.expire(key, ttl)
