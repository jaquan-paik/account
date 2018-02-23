from typing import Callable

from django.core.cache import cache
from django.utils.decorators import decorator_from_middleware_with_args

from lib.log.logger import logger
from .middlewares import DynamicKeyPrefixCacheMiddleware


def cache_for(key: str, get_ttl_fn: Callable = None):
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            result = cache.get(key, None)
            if result is None:
                logger.debug('Cache miss: %s', key)
                result = func(*args, **kwargs)
                ttl = get_ttl_fn() if get_ttl_fn is not None else 3600
                cache.set(key, result, ttl)
            return result

        return _wrapper

    return _decorator


def cache_page(cache_timeout, get_key_prefix=None):
    return decorator_from_middleware_with_args(DynamicKeyPrefixCacheMiddleware)(cache_timeout=cache_timeout, get_key_prefix=get_key_prefix)
