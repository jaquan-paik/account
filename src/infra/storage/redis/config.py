from django.conf import settings


class RedisConfig:
    @staticmethod
    def get_host() -> str:
        return settings.REDIS_HOST

    @staticmethod
    def get_port() -> int:
        return settings.REDIS_PORT
