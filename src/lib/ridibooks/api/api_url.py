from infra.configure.config import GeneralConfig

_DEV_RIDI_STORE_DOMAIN = 'https://shelf.dev.ridi.io'
_PROD_RIDI_STORE_DOMAIN = 'https://ridibooks.com'


class RidiApiUrl:
    @classmethod
    def get_url(cls, url: str) -> str:
        return cls._get_domain() + url

    @classmethod
    def _get_domain(cls) -> str:
        return cls._get_dev_domain() if GeneralConfig.is_dev() else cls._get_prod_domain()

    @classmethod
    def _get_prod_domain(cls):
        raise NotImplementedError

    @classmethod
    def _get_dev_domain(cls):
        raise NotImplementedError


class RidiStoreApiUrl(RidiApiUrl):
    ACCOUNT_INFO = '/api/account/info'

    @classmethod
    def _get_prod_domain(cls):
        return _PROD_RIDI_STORE_DOMAIN

    @classmethod
    def _get_dev_domain(cls):
        return _DEV_RIDI_STORE_DOMAIN
