from datetime import datetime, timedelta

from django.http import Http404, HttpResponseForbidden

from infra.network.constants.custom_header import CustomHttpHeader
from .encrypt import CryptoHelper


def certified_internal_api(key):
    def _decorator(view_func):
        def _wrapper(self, request, *args, **kwargs):
            internal_api_key = request.META.get(CustomHttpHeader.INTERNAL_API_KEY_HEADER)
            if internal_api_key is None:
                return Http404()

            token_time = CryptoHelper(key).decrypt(internal_api_key)
            token_time_diff = datetime.now() - datetime.fromtimestamp(int(token_time))

            if token_time_diff > timedelta(minutes=10):
                return HttpResponseForbidden()

            return view_func(self, request, *args, **kwargs)
        return _wrapper
    return _decorator
