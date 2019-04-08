from django.core.exceptions import ObjectDoesNotExist

from apps.domains.account.models import User
from apps.domains.oauth2.exceptions import InvalidRefreshToken
from apps.domains.oauth2.models import Application as Client, RefreshToken
from apps.domains.oauth2.repositories.refresh_token_repository import RefreshTokenRepository


class RefreshTokenService:
    @staticmethod
    def generate(client: Client, user: User, scope: str) -> str:
        refresh_token = RefreshTokenRepository.create_refresh_token(client, user, scope)
        return refresh_token.token

    @staticmethod
    def get_by_token(token: str) -> RefreshToken:
        try:
            return RefreshTokenRepository.get_by_token(token)
        except ObjectDoesNotExist:
            raise InvalidRefreshToken
