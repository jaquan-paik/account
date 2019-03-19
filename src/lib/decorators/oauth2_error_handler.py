from django.http import JsonResponse
from oauthlib.oauth2 import OAuth2Error

from lib.base.response import get_template_response


def oauth2_error_handler(return_template=False):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            try:
                return func(self, request, *args, **kwargs)
            except OAuth2Error as e:
                if return_template:
                    return get_template_response(request, e.error, e.description, e.status_code)
                return JsonResponse(data={"error": e.error, "description": e.description}, status=e.status_code)

        return wrapper

    return decorator
