from django.http import HttpResponseForbidden

from lib.utils.ip import get_client_ip_from_request, is_internal_ip
from .ridi_ip import RidiIP


def ridi_ip_required(func=None):
    def _decorator(_func):
        def _wrapped_view(request, *args, **kwargs):
            client_ip = get_client_ip_from_request(request)

            if not is_internal_ip(client_ip) and not RidiIP.is_ridi_ip(client_ip):
                return HttpResponseForbidden()

            return _func(request, *args, **kwargs)

        return _wrapped_view

    return _decorator(func)
