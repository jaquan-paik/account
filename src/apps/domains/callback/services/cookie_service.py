
from apps.domains.callback.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY
from apps.domains.callback.dtos import TokenData
from apps.domains.callback.helpers.url_helper import UrlHelper


class CookieService:
    @classmethod
    def add_token_cookie(cls, response, access_token: TokenData, refresh_token: TokenData):
        cls._set_token_cookie(response, ACCESS_TOKEN_COOKIE_KEY, access_token)
        cls._set_token_cookie(response, REFRESH_TOKEN_COOKIE_KEY, refresh_token)

    @classmethod
    def clear_token_cookie(cls, response):
        cls._remove_token_cookie(response, ACCESS_TOKEN_COOKIE_KEY)
        cls._remove_token_cookie(response, REFRESH_TOKEN_COOKIE_KEY)

    @classmethod
    def _set_token_cookie(cls, response, key: str, token_data: TokenData):
        # Dev의 경우 root_domain (dev.ridi.io / dev.ridi.com) 두 가지를 지원해야함.
        for root_domain in UrlHelper.get_root_domains():
            response.set_cookie(
                key, token_data.token, max_age=token_data.expires_in, expires=token_data.cookie_expire_time,
                domain=root_domain, secure=True, httponly=True
            )

    @classmethod
    def _remove_token_cookie(cls, response, key: str):
        # Dev의 경우 root_domain (dev.ridi.io / dev.ridi.com) 두 가지를 지원해야함.
        for root_domain in UrlHelper.get_root_domains():
            response.set_cookie(
                key, '', max_age=0, expires='Thu, 01-Jan-1970 00:00:00 GMT', domain=root_domain, secure=True, httponly=True
            )
