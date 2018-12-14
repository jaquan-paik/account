import typing

from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper

RESPONSE_HANDLER_TYPE = typing.Optional[typing.Callable]
EMPTY_TOKENS = (False, False)


def add_tokens_in_cookie(func):
    def wrapper(self, request, *args, **kwargs):
        response, (access_token, refresh_token) = func(self, request, *args, **kwargs)
        root_domain = UrlHelper.get_root_domain(request)
        if access_token and refresh_token:
            ResponseCookieHelper.add_token_cookie(
                response=response, access_token=access_token, refresh_token=refresh_token, root_domain=root_domain
            )
        return response

    return wrapper


def clear_tokens_in_cookie(func):
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        root_domain = UrlHelper.get_root_domain(request)
        ResponseCookieHelper.clear_token_cookie(response, root_domain)
        return response

    return wrapper
