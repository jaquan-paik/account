from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from lib.ridibooks.api.store import StoreApi
from lib.ridibooks.common.exceptions import RidibooksException


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ridibooks_session_id = request.COOKIES.get('PHPSESSID', None)

        user = AnonymousUser()

        if ridibooks_session_id is not None:
            try:
                account_info = StoreApi(phpsession_id=ridibooks_session_id).get_account_info()
            except RidibooksException:
                pass
            else:
                user, _ = get_user_model().objects.get_or_create(idx=account_info['result']['idx'], id=account_info['result']['id'])

        request.user = user
