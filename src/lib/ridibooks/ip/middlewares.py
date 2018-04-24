from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from lib.utils.ip import get_client_ip_from_request, is_internal_ip
from .constants import RidiIP


class RidiIPFilterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        client_ip = get_client_ip_from_request(request)

        if not is_internal_ip(client_ip) and not RidiIP.is_ridi_ip(client_ip):
            return HttpResponseForbidden()
        return None
