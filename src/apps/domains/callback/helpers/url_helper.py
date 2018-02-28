from django.urls import reverse

from infra.configure.config import GeneralConfig


class UrlHelper:
    @staticmethod
    def get_redirect_uri():
        return f'https://{GeneralConfig.get_site_domain()}{reverse("callback:callback")}'

    @staticmethod
    def get_token():
        return f'https://{GeneralConfig.get_site_domain()}{reverse("oauth2_provider:token")}'
