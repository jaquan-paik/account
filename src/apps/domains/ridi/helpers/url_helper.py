from django.conf import settings
from django.urls import reverse

from apps.domains.ridi.exceptions import NotAllowedRootDomainException
from infra.configure.config import GeneralConfig
from lib.cache.memorize import memorize
from lib.utils.url import generate_query_url


class UrlHelper:
    @staticmethod
    @memorize
    def get_callback_view_url() -> str:
        return f'https://{GeneralConfig.get_site_domain()}{reverse("ridi:callback")}'

    @staticmethod
    @memorize
    def get_oauth2_token_url() -> str:
        return f'https://{GeneralConfig.get_site_domain()}{reverse("oauth2_provider:token")}'

    @classmethod
    @memorize
    def get_redirect_url(cls, in_house_redirect_uri: str, client_id: str) -> str:
        return generate_query_url(cls.get_callback_view_url(), {'in_house_redirect_uri': in_house_redirect_uri, 'client_id': client_id})

    @staticmethod
    @memorize
    def get_root_uri() -> str:
        return GeneralConfig.get_store_url()

    @staticmethod
    def get_allowed_cookie_root_domain(request) -> str:
        if settings.COOKIE_ROOT_DOMAIN in request.get_host():
            return settings.COOKIE_ROOT_DOMAIN

        raise NotAllowedRootDomainException('허용하지 않는 루트도메인입니다.')
