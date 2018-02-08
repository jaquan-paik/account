from datetime import datetime

from django.utils.cache import get_conditional_response
from django.utils.http import parse_http_date_safe

from infra.network.constants.custom_header import CustomHttpHeader
from .decorators import cache_page


class CachePageMixin:
    PAGE_CACHE_TTL = 60
    INVALIDATE_CACHE_HOURLY = True

    @classmethod
    def get_key_prefix(cls, request) -> str:
        version = request.META.get(CustomHttpHeader.API_VERSION_HEADER) or '1'
        key_prefix = 'apiv_' + version
        if cls.INVALIDATE_CACHE_HOURLY is True:
            key_prefix += datetime.now().strftime('%H')
        return key_prefix

    @classmethod
    def as_view(cls, **initkwargs):
        return cache_page(cls.PAGE_CACHE_TTL, get_key_prefix=cls.get_key_prefix)(super().as_view(**initkwargs))


class ConditionalCachePageMixin(CachePageMixin):
    @classmethod
    def as_view(cls, **initkwargs):
        real_view_func = super().as_view(**initkwargs)

        def view_func(request, **kwargs):
            response = real_view_func(request, **kwargs)

            if request.method != 'GET':
                return response

            etag = response.get('ETag')
            last_modified = response.get('Last-Modified')
            if last_modified:
                last_modified = parse_http_date_safe(last_modified)
            if etag or last_modified:
                return get_conditional_response(
                    request,
                    etag=etag,
                    last_modified=last_modified,
                    response=response,
                )

            return response
        return view_func
