from apps.domains.callback.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY
from apps.domains.callback.dtos import TokenData
from apps.domains.callback.exceptions import NotAllowedRootDomainException
from infra.configure.config import GeneralConfig


class CookieService:
    @classmethod
    def add_token_cookie(cls, request, response, access_token: TokenData, refresh_token: TokenData):
        cls._set_token_cookie(request, response, ACCESS_TOKEN_COOKIE_KEY, access_token)
        cls._set_token_cookie(request, response, REFRESH_TOKEN_COOKIE_KEY, refresh_token)

    @classmethod
    def clear_token_cookie(cls, request, response):
        cls._remove_token_cookie(request, response, ACCESS_TOKEN_COOKIE_KEY)
        cls._remove_token_cookie(request, response, REFRESH_TOKEN_COOKIE_KEY)

    @classmethod
    def _set_token_cookie(cls, request, response, key: str, token_data: TokenData):
        response.set_cookie(
            key, token_data.token, max_age=token_data.expires_in, expires=token_data.cookie_expire_time,
            domain=cls._get_root_domain(request), secure=True, httponly=True
        )

    @classmethod
    def _remove_token_cookie(cls, request, response, key: str):
        response.set_cookie(
            key, '', max_age=0, expires='Thu, 01-Jan-1970 00:00:00 GMT', domain=cls._get_root_domain(request), secure=True, httponly=True
        )

    @classmethod
    def _get_root_domain(cls, request):
        current_domain = request.get_host()

        domains = GeneralConfig.get_root_domain_whitelist()
        for domain in domains:
            if domain in current_domain:
                return domain

        raise NotAllowedRootDomainException()
