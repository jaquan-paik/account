from typing import Callable
from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper


def clear_tokens_in_cookie(func: Callable):
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        ResponseCookieHelper.clear_token_cookie(response)
        return response

    return wrapper
