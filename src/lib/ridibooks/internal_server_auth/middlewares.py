from django.utils.deprecation import MiddlewareMixin

from lib.ridibooks.common.constants import HTTP_AUTHORIZATION_HEADER
from lib.ridibooks.common.response import HttpUnauthorized
from lib.ridibooks.internal_server_auth.helpers.internal_server_auth_helper import InternalServerAuthHelper
from lib.ridibooks.internal_server_auth.utils import TokenHandler


class RidiInternalAuthMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        token = request.META.get(HTTP_AUTHORIZATION_HEADER)
        if token is None:
            return HttpUnauthorized()

        if not InternalServerAuthHelper.verify(token=TokenHandler.parse(token)):
            return HttpUnauthorized()

        return None
