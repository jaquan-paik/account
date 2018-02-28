from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from apps.domains.callback.helpers.client_helper import ClientHelper
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
    def client(self):
        if self._client is None:
            try:
                self._client = ClientHelper.get_client(self.client_id)
            except ObjectDoesNotExist:
                PermissionDenied()
        return self._client

    def validate_params(self):
        if self.redirect_uri is None:
            raise PermissionDenied()

        if self.client_id is None:
            raise PermissionDenied()

    def validate_state(self, state: str):
        if state != self.state:
            raise PermissionDenied()

    def validate_client(self):
        #  내부 서비스가 아니면 해당 방법을 사용할 수 없다.
        if not self.client.is_in_house:
            raise PermissionDenied()


class TokenData:
    def __init__(self, token: str, expires_in: int):
        self.token = token
        self.expires_in = expires_in
        self.cookie_expire_time = generate_cookie_expire_time(expires_in)
