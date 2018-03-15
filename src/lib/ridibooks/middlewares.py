from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from lib.ridibooks.utils import is_ridi_ip_from_request
from .api.api_helper import RidiApiHelper
from .exceptions import RidibooksException

UserModel = get_user_model()


class RidiIPFilterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not is_ridi_ip_from_request(request):
            return HttpResponseForbidden()
        return None


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ridibooks_session_id = request.COOKIES.get('PHPSESSID', None)

        user = AnonymousUser()

        try:
            account_info = RidiApiHelper(phpsession_id=ridibooks_session_id).get_account_info()
        except RidibooksException:
            pass
        else:
            user, _ = UserModel.objects.get_or_create(idx=account_info['result']['idx'], id=account_info['result']['id'])

        request.user = user
