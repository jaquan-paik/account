from django.conf import settings

from ridi.cms.config import Config


class _Settings:
    CMS_RPC_URL = 'RIDI_CMS_RPC_URL'


config = Config()
config.RPC_URL = getattr(settings, _Settings.CMS_RPC_URL)


class CmsConfig:
    @staticmethod
    def get_config() -> Config:
        return config
