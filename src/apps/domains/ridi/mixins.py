from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.url_helper import UrlHelper
from lib.django.views.cookie.mixins import CookieMixin
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY


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
