from typing import Optional

from apps.domains.callback.dtos import OAuth2Data, TokenData
from apps.domains.callback.helpers.url_helper import UrlHelper
from lib.django.views.cookie.mixins import CookieMixin
from lib.django.views.session.mixins import SessionMixin
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY

SESSION_STATE_KEY = 'oauth2.state'
SESSION_CLIENT_ID_KEY = 'oauth2.client_id'
SESSION_REDIRECT_URI_KEY = 'oauth2.redirect_uri'


class TokenCookieMixin(CookieMixin):
    def add_token_cookie(self, response, access_token: TokenData, refresh_token: TokenData, root_domain: str):
        self.set_cookie(
            response=response, key=ACCESS_TOKEN_COOKIE_KEY, value=access_token.token, domain=root_domain,
            expires_in=access_token.expires_in, expires_date=access_token.cookie_expire_time,
        )
        self.set_cookie(
            response=response, key=REFRESH_TOKEN_COOKIE_KEY, value=refresh_token.token, domain=root_domain,
            expires_in=refresh_token.expires_in, expires_date=refresh_token.cookie_expire_time,
        )

    def clear_token_cookie(self, response, root_domain: str):
        self.clear_cookie(response=response, key=ACCESS_TOKEN_COOKIE_KEY, domain=root_domain)
        self.clear_cookie(response=response, key=REFRESH_TOKEN_COOKIE_KEY, domain=root_domain)

    def get_root_domain(self) -> str:
        return UrlHelper.get_root_domain(self.request)


class OAuth2SessionMixin(SessionMixin):
    def get_oauth2_data(self, code: str, state: Optional[str]=None) -> OAuth2Data:
        oauth2_data = OAuth2Data(
            self.get_session(key=SESSION_STATE_KEY),
            self.get_session(key=SESSION_CLIENT_ID_KEY),
            self.get_session(key=SESSION_REDIRECT_URI_KEY),
        )
        oauth2_data.code = code
        self.validate_oauth2_data(oauth2_data=oauth2_data, is_valid_state=True, state=state)

        return oauth2_data

    def set_oauth2_data(self, client_id: str, redirect_uri: str, state: Optional[str]):
        oauth2_data = OAuth2Data(state, client_id, redirect_uri)
        self.validate_oauth2_data(oauth2_data=oauth2_data)

        self.set_session(key=SESSION_CLIENT_ID_KEY, value=client_id)
        self.set_session(key=SESSION_REDIRECT_URI_KEY, value=redirect_uri)
        self.set_session(key=SESSION_STATE_KEY, value=state)

    def validate_oauth2_data(self, oauth2_data: OAuth2Data, is_valid_state: bool=False, state: Optional[str]=None):
        oauth2_data.validate_client()
        oauth2_data.validate_redirect_uri()

        if is_valid_state:
            oauth2_data.validate_state(state=state)
