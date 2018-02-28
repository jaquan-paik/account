from django.core.exceptions import PermissionDenied

from lib.utils.date import generate_cookie_expire_time


class OAuth2Data:
    def __init__(self, state: str, client_id: str, redirect_uri: str):
        self.state = state
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.code = None

    def validate(self, state: str):
        if self.redirect_uri is None:
            raise PermissionDenied()

        if self.client_id is None:
            raise PermissionDenied()

        if state != self.state:
            raise PermissionDenied()


class TokenData:
    def __init__(self, token: str, expires_in: int):
        self.token = token
        self.expires_in = expires_in
        self.cookie_expire_time = generate_cookie_expire_time(expires_in)
