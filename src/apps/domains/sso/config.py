from django.conf import settings


class SSOConfig:
    @staticmethod
    def get_sso_root_domain():
        return settings.SSO_ROOT_DOMAIN

    @staticmethod
    def get_crypto_key(hint: str) -> str:
        return settings.SSO_CRYPTO_KEYS[hint]
