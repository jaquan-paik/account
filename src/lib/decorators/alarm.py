from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Union

from lib.log import sentry
from lib.log.logger import logger


class LogExecuteKey:
    STORE_API_ACCOUNT_INFO = 'STORE_API_ACCOUNT_INFO'
    STORE_API_ACCOUNT_IS_LOGINABLE = 'STORE_API_ACCOUNT_IS_LOGINABLE'


def process_time_limit(**kwargs):
    def _decorator(func: Callable):
        def _wrapper(*_args, **_kwargs):
            start_datetime = datetime.now()
            value = func(*_args, **_kwargs)

            delta = datetime.now() - start_datetime
            if delta > timedelta(**kwargs):
                sentry.message('[INFO] ALARM: %s' % func.__name__)

            return value

        return wraps(func)(_wrapper)

    return _decorator


def log_execute_time(
        key: str, timeout: Union[int, float], always: bool = True, with_sentry: bool = False, with_sentry_if_exceeded: bool = False
):
    def _decorator(func: Callable):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            start_datetime = datetime.now()

            try:
                val = func(*args, **kwargs)
            finally:
                delta = datetime.now() - start_datetime
                exceeded = delta > timedelta(seconds=timeout)

                if always or exceeded:
                    msg = f'[EXECUTE] {key}'
                    extra = {
                        'exec_key': key,
                        'exec_timeout': timeout,
                        'exec_time': delta.total_seconds()
                    }

                    logger.info(msg, extra=extra)

                    if with_sentry or (with_sentry_if_exceeded and exceeded):
                        sentry.message(msg, extra=extra)

            return val

        return _wrapper

    return _decorator
