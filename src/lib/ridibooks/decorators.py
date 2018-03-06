from django.http import HttpResponseForbidden

from lib.ridibooks.utils import is_ridi_ip_from_request


def ridi_ip_required(func=None):
    def _decorator(_func):
        def _wrapped_view(request, *args, **kwargs):
            if not is_ridi_ip_from_request(request):
                return HttpResponseForbidden()

            return _func(request, *args, **kwargs)

        return _wrapped_view

    return _decorator(func)
