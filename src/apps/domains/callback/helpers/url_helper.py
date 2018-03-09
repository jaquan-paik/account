from django.urls import reverse

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
