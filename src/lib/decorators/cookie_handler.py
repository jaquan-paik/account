from typing import Callable
from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper


def clear_tokens_in_cookie(func: Callable):
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        root_domain = UrlHelper.get_allowed_cookie_root_domain(request)
        ResponseCookieHelper.clear_token_cookie(response, root_domain)
        return response

    return wrapper
