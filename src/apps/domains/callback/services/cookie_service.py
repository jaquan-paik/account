
from apps.domains.callback.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY
from apps.domains.callback.dtos import TokenData


class CookieService:
    @classmethod
    def add_token_cookie(cls, response, access_token: TokenData, refresh_token: TokenData, root_domain: str):
        cls._set_token_cookie(response, ACCESS_TOKEN_COOKIE_KEY, access_token, root_domain)
        cls._set_token_cookie(response, REFRESH_TOKEN_COOKIE_KEY, refresh_token, root_domain)

    @classmethod
    def clear_token_cookie(cls, response, root_domain: str):
        cls._remove_token_cookie(response, ACCESS_TOKEN_COOKIE_KEY, root_domain)
        cls._remove_token_cookie(response, REFRESH_TOKEN_COOKIE_KEY, root_domain)

    @classmethod
    def _set_token_cookie(cls, response, key: str, token_data: TokenData, root_domain):
        response.set_cookie(
            key, token_data.token, max_age=token_data.expires_in, expires=token_data.cookie_expire_time,
            domain=root_domain, secure=True, httponly=True
        )

    @classmethod
    def _remove_token_cookie(cls, response, key: str, root_domain: str):
        response.set_cookie(
            key, '', max_age=0, expires='Thu, 01-Jan-1970 00:00:00 GMT', domain=root_domain, secure=True, httponly=True
        )
