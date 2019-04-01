from apps.domains.sso.config import SSOConfig
from apps.domains.sso.exceptions import NotFoundSSOKeyException


class SSOKeyService:

    @staticmethod
    def get_key(hint: str) -> str:
        try:
            return SSOConfig.get_crypto_key(hint)
        except KeyError:
            raise NotFoundSSOKeyException('SSO 키를 찾을 수 없습니다.')
