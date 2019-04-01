from django.conf import settings


class SSOCryptoConfig:
    @staticmethod
    def get_key(hint: str) -> str:
        return settings.SSO_CRYPTO_KEYS[hint]
