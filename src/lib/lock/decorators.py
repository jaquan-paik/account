from datetime import datetime, timedelta

from filelock import FileLock, Timeout

from infra.network.constants.api_status_code import ApiStatusCodes
from lib.log import sentry
from lib.log.logger import logger
from .helper import LockHelper, LockKeyGenerator


def lock(key_prefix=None, lock_ttl=LockHelper.DEFAULT_TTL):
    def _decorator(view_func):
        def _wrapper(self, request, *args, **kwargs):
            customer = request.user
            if not customer.is_authenticated:
                return view_func(self, request, *args, **kwargs)

            lock_helper = LockHelper(LockKeyGenerator.get_api_key_maker(key_prefix, customer.id), lock_ttl)
            if not lock_helper.lock():
                sentry.error_message('[API중복요청] %s - %s' % (request.path, lock_helper.key))
                return self.fail_response(message='중복 요청을 했습니다.', code=ApiStatusCodes.X_400_DUPLICATE_API)

            response = view_func(self, request, *args, **kwargs)

            lock_helper.unlock()
            return response

        return _wrapper

    return _decorator


def f_lock(key_prefix: str, lock_ttl: int = 600, lock_waiting_timeout: int = 0):
    def _decorator(_func):
        def _wrapped_view(request, *args, **kwargs):
            key = f'{key_prefix}.lock'
            _lock = FileLock(key, timeout=lock_ttl)
            start = datetime.now()

            try:
                _lock.acquire(timeout=lock_waiting_timeout)

            except Timeout:
                return None

            try:
                return _func(request, *args, **kwargs)

            finally:
                _lock.release()
                end = datetime.now()
                time_taken = end - start

                if time_taken > timedelta(seconds=lock_ttl):
                    logger.error(f'[LOCK] {key} is over lock ttl. - {time_taken} sec.')

                elif time_taken > timedelta(seconds=lock_ttl * 0.5):
                    logger.error(f'[LOCK] Be careful! {key} is over lock ttl margin. - {time_taken} sec.')

        return _wrapped_view

    return _decorator
