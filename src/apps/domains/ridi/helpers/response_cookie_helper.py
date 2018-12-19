from apps.domains.ridi.dtos import TokenData
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY

EPOCH_TIME = 'Thu, 01-Jan-1970 00:00:00 GMT'


class ResponseCookieHelper:
    @classmethod
    def add_token_cookie(cls, response, access_token: TokenData, refresh_token: TokenData, root_domain: str):
        cls.set_secure_cookie(
            response, key=ACCESS_TOKEN_COOKIE_KEY, value=access_token.token, domain=root_domain,
            expires_in=access_token.expires_in, expires_date=access_token.cookie_expire_time,
        )
        cls.set_secure_cookie(
            response, key=REFRESH_TOKEN_COOKIE_KEY, value=refresh_token.token, domain=root_domain,
            expires_in=refresh_token.expires_in, expires_date=refresh_token.cookie_expire_time,
        )

    @staticmethod
    def set_secure_cookie(response, key: str, value: str, domain: str, **kwargs):
        response.set_cookie(
            key, value, max_age=kwargs.get('expires_in', None), expires=kwargs.get('expires_date', None),
            domain=domain, secure=True, httponly=True
        )

    @staticmethod
    def clear_cookie(response, key: str, domain: str):
        response.set_cookie(
            key, '', max_age=0, expires=EPOCH_TIME, domain=domain, secure=True, httponly=True
        )

    @classmethod
    def clear_token_cookie(cls, response, root_domain: str):
        cls.clear_cookie(response, key=ACCESS_TOKEN_COOKIE_KEY, domain=root_domain)
        cls.clear_cookie(response, key=REFRESH_TOKEN_COOKIE_KEY, domain=root_domain)
