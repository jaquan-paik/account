from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from lib.ridibooks.api.api_helper import RidiApiHelper
from lib.ridibooks.api.exceptions import RidibooksException


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ridibooks_session_id = request.COOKIES.get('PHPSESSID', None)

        user = AnonymousUser()
        try:
            account_info = RidiApiHelper(phpsession_id=ridibooks_session_id).get_account_info()
        except RidibooksException:
            pass
        else:
            user, _ = get_user_model().objects.get_or_create(idx=account_info['result']['idx'], id=account_info['result']['id'])

        request.user = user
