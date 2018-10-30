from datetime import datetime, timedelta
from urllib.parse import urlparse

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from apps.domains.callback.helpers.client_helper import ClientHelper
from apps.domains.oauth2.models import Application
from lib.log import sentry
from lib.utils.date import generate_cookie_expire_time


class OAuth2Data:
    def __init__(self, state: str, client_id: str, redirect_uri: str):
        self.state = state
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.code = None
        self._client = None

        self.validate_params()

    @property
    def client(self) -> Application:
        if self._client is None:
            try:
                self._client = ClientHelper.get_client(self.client_id)
            except ObjectDoesNotExist:
                raise PermissionDenied()
        return self._client

    def validate_params(self):
        if self.redirect_uri is None:
            sentry.error_message(f'[PermissionDenied][validate_params]')
            raise PermissionDenied()

        if self.client_id is None:
            raise PermissionDenied()

    def validate_state(self, state: str):
        if state != self.state:
            sentry.error_message(f'[PermissionDenied][validate_state]')
            raise PermissionDenied()

    def validate_client(self):
        #  내부 서비스가 아니면 해당 방법을 사용할 수 없다.
        if not self.client.is_in_house:
            sentry.error_message(f'[PermissionDenied][validate_client]')
            raise PermissionDenied()

    def validate_redirect_uri(self):
        if not self.client.is_in_house:
            sentry.error_message(f'[PermissionDenied][validate_redirect_uri][client][is_in_house]')
            raise PermissionDenied()

        if not self._is_allowed_uri(self.redirect_uri):
            sentry.error_message(f'[PermissionDenied][validate_redirect_uri][_is_allowed_uri] {self.redirect_uri}')
            raise PermissionDenied()

    def _is_allowed_uri(self, uri: str) -> bool:
        parsed_uri = urlparse(uri)
        for allowed_uri in self.client.redirect_uris.split():
            parsed_allowed_uri = urlparse(allowed_uri)

            if parsed_allowed_uri.scheme == parsed_uri.scheme and parsed_allowed_uri.netloc == parsed_uri.netloc:
                return True
        return False


class TokenData:
    def __init__(self, token: str, expires_in: int):
        now = datetime.now()

        self.token = token
        self.expires_in = expires_in
        self.expires_at = int((now + timedelta(seconds=expires_in)).timestamp())
        self.cookie_expire_time = generate_cookie_expire_time(expires_in, now)
