from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from apps.domains.account.services.account_info_service import AccountInfoService
from apps.domains.callback.constants import CookieRootDomains
from lib.ridibooks.api.store import StoreApi
from lib.ridibooks.common.constants import PHP_SESSION_COOKIE_KEY
from lib.ridibooks.common.exceptions import RidibooksException


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ridibooks_session_id = request.COOKIES.get(PHP_SESSION_COOKIE_KEY, None)

        user = AnonymousUser()

        if ridibooks_session_id is not None:

            try:
                account_info = AccountInfoService.get_account_info_by_ridibooks_session_id(request.get_host(), ridibooks_session_id)

            except RidibooksException:
                pass

            else:
                user, _ = get_user_model().objects.get_or_create(idx=account_info['result']['idx'], id=account_info['result']['id'])

        request.user = user
