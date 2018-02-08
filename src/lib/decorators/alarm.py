from datetime import datetime, timedelta
from functools import wraps
from typing import Callable

from lib.log import sentry


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
