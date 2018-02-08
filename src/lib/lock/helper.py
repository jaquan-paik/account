import uuid

from infra.storage.redis.constants import RedisDatabase
from infra.storage.redis.managers import RedisManager


class LockKeyGenerator:
    """
    _LOCK_KEY = 'lk:'

    @staticmethod
    def get_lock_key(user_id: int) -> str:
        return LockKeyGenerator._LOCK_KEY + str(user_id)
    """

    @staticmethod
    def get_api_key_maker(prefix: str, customer_id: int) -> str:
        return prefix + str(customer_id)


class RedisLockManager(RedisManager):
    database = RedisDatabase.LOCK

    def set_key(self, key: str, value: str, ttl: int) -> bool:
        return self.set_nx_ex(key, value, ttl)

    def delete_key(self, key: str) -> bool:
        return self.delete(key)

    def extend_ttl(self, key: str, ttl: int) -> bool:
        return self.expire(key, ttl)

    def is_locked(self, key: str) -> bool:
        conn = self.get_connection()
        lock_value = conn.get(key)
        return lock_value is not None


class LockHelper:
    # 기본 작업 시간 60 초
    # Lock 은 무한히 잡을 수 없다.
    DEFAULT_TTL = 60

    lock_manager = RedisLockManager()

    def __init__(self, key: str, ttl=DEFAULT_TTL):
        self.key = key
        self.uuid = uuid.uuid4().hex
        self.ttl = ttl

    def lock(self) -> bool:
        return self.lock_manager.set_key(self.key, self.uuid, self.ttl)

    def unlock(self) -> bool:
        result = self.lock_manager.delete_key(self.key)
        if result:
            self.uuid = None
        return result

    def ping(self) -> bool:
        return self.lock_manager.extend_ttl(self.key, self.ttl)

    def is_locked(self) -> bool:
        return self.lock_manager.is_locked(self.key)
