from django.urls import reverse

from apps.domains.callback.constants import CookieRootDomains
from apps.domains.callback.exceptions import NotAllowedRootDomainException
from infra.configure.config import GeneralConfig
from lib.cache.memorize import memorize


class UrlHelper:
    @staticmethod
    @memorize
    def get_redirect_uri():
        return f'https://{GeneralConfig.get_site_domain()}{reverse("ridi:callback")}'

    @staticmethod
    @memorize
    def get_token():
        return f'https://{GeneralConfig.get_site_domain()}{reverse("oauth2_provider:token")}'

    @staticmethod
    @memorize
    def get_root_uri():
        return f'https://{GeneralConfig.get_store_url()}'

    @staticmethod
    def get_root_domain(request) -> str:
        host = request.get_host()
        root_domains = CookieRootDomains.get_root_whitelist(debug=GeneralConfig.is_dev())

        for root_domain in root_domains:
            if root_domain in host:
                return root_domain

        raise NotAllowedRootDomainException('허용하지 않는 루트도메인입니다.')
