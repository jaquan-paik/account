import uuid
from datetime import timedelta, datetime

from apps.domains.account.models import User
from apps.domains.oauth2.constants import REFRESH_TOKEN_EXPIRE_DAYS
from apps.domains.oauth2.models import RefreshToken, Application as Client


class RefreshTokenRepository:
    @staticmethod
    def create_refresh_token(client: Client, user: User, scope: str) -> RefreshToken:
        token = uuid.uuid4().hex
        expires = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        refresh_token = RefreshToken(application=client, user=user, scope=scope, token=token, expires=expires)
        refresh_token.save()
        return refresh_token

    @staticmethod
    def get_by_token(token: str) -> RefreshToken:
        return RefreshToken.objects.get(token=token)
