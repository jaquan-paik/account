from django.utils.deprecation import MiddlewareMixin

from .services import add_log


class AdminAccessLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            add_log(user.id, request.method, request.path)
