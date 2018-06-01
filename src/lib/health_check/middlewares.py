from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from lib.health_check.check_database import CheckDatabase


class HealthCheckerMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        if request.path != '/health':
            return None

        CheckDatabase.check()

        service_status = {
            'message': 'All is well.',
        }

        return JsonResponse(service_status, status=200)
