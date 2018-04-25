from django.utils.deprecation import MiddlewareMixin

from lib.ridibooks.internal_server_auth.helpers.jwt_auth import JwtAuthHelper
from lib.ridibooks.common.constants import HTTP_AUTHORIZATION_HEADER
from lib.ridibooks.common.response import HttpUnauthorized


class RidiInternalAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get(HTTP_AUTHORIZATION_HEADER)
        if token is None:
            return HttpUnauthorized()

        if not JwtAuthHelper.verify(token=token):
            return HttpUnauthorized()

        return None
