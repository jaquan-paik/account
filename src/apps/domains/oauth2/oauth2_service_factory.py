from typing import Tuple

from apps.domains.oauth2.constants import GrantType
from apps.domains.oauth2.serializers import AuthorizationCodeGrantSerializer, PasswordGrantSerializer, RefreshTokenGrantSerializer
from apps.domains.oauth2.services.oauth2_authorization_code_service import OAuth2AuthorizationCodeService
from apps.domains.oauth2.services.oauth2_password_service import OAuth2PasswordTokenService
from apps.domains.oauth2.services.oauth2_refresh_token_service import OAuth2RefreshTokenService


class OAuth2TokenServiceFactory:

    @staticmethod
    def create_serializer_and_service(grant_type: str, data: dict) -> Tuple:
        if grant_type == GrantType.AUTHORIZATION_CODE:
            return AuthorizationCodeGrantSerializer(data=data), OAuth2AuthorizationCodeService

        if grant_type == GrantType.PASSWORD:
            return PasswordGrantSerializer(data=data), OAuth2PasswordTokenService

        if grant_type == GrantType.REFRESH_TOKEN:
            return RefreshTokenGrantSerializer(data=data), OAuth2RefreshTokenService

        return None, None
