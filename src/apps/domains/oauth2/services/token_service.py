from typing import List

from apps.domains.account.models import User
from apps.domains.oauth2.constants import ACCESS_TOKEN_EXPIRE_SECONDS, TOKEN_TYPE, REFRESH_TOKEN_EXPIRE_SECONDS
from apps.domains.oauth2.models import Application as Client
from apps.domains.oauth2.services.access_token_service import AccessTokenService
from apps.domains.oauth2.services.refresh_token_service import RefreshTokenService


class TokenService:
    @staticmethod
    def generate(client: Client, user: User, scopes: List[str]) -> dict:
        scope = ' '.join(scopes)
        access_token = AccessTokenService.generate(client, user, scope)
        refresh_token = RefreshTokenService.generate(client, user, scope)
        return {
            "access_token": access_token,
            "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
            "token_type": TOKEN_TYPE,
            "scope": scope,
            "refresh_token": refresh_token,
            "refresh_token_expires_in": REFRESH_TOKEN_EXPIRE_SECONDS
        }
