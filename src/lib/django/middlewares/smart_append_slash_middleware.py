from django import http
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin


class SmartAppendSlashMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.path_info.endswith('/') and not self._resolves(request.path_info) and self._resolves(request.path_info + '/'):
            request.path_info += '/'

        return None

    @staticmethod
    def _resolves(url: str) -> bool:
        try:
            resolve(url)
            return True
        except http.Http404:
            return False
