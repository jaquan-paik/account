from apps.domains.account.models import User
from apps.domains.oauth2.models import RefreshToken, Application as Client


class RefreshTokenRepository:
    @staticmethod
    def create_refresh_token(client: Client, user: User, scope: str) -> RefreshToken:
        refresh_token = RefreshToken(application=client, user=user, scope=scope)
        refresh_token.save()
        return refresh_token

    @staticmethod
    def get_by_token(token: str) -> RefreshToken:
        return RefreshToken.objects.get(token=token)
