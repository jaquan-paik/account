from django.conf import settings


class SSOConfig:
    @staticmethod
    def get_sso_redirect_domain():
        return settings.SSO_REDIRECT_DOMAIN

    @staticmethod
    def get_sso_login_url():
        return settings.SSO_LOGIN_URL

    @staticmethod
    def get_crypto_key(hint: str) -> str:
        return settings.SSO_CRYPTO_KEYS[hint]
