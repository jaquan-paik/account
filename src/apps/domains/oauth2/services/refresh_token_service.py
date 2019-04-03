from apps.domains.account.models import User
from apps.domains.oauth2.models import Application as Client
from apps.domains.oauth2.repositories.refresh_token_repository import RefreshTokenRepository


class RefreshTokenService:
    @staticmethod
    def generate(client: Client, user: User, scope: str) -> str:
        refresh_token = RefreshTokenRepository.create_refresh_token(client, user, scope)
        return refresh_token.token
