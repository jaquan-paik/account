from typing import Callable

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from requests import HTTPError

from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper
from lib.django.http.response import HttpResponseUnauthorized


def return_json_response_if_http_error_raised(func: Callable):
    def _wrapper(self, request, *args, **kwargs):
        try:
            return func(self, request, *args, **kwargs)
        except HTTPError as e:
            return JsonResponse(data=e.response.json(), status=e.response.status_code)

    return _wrapper


def clear_tokens_if_permission_denied_raised(func: Callable):
    def wrapper(self, request, *args, **kwargs):
        try:
            return func(self, request, *args, **kwargs)
        except PermissionDenied:
            response = HttpResponseUnauthorized()
            root_domain = UrlHelper.get_root_domain(request)
            ResponseCookieHelper.clear_token_cookie(response, root_domain)
            return response

    return wrapper
