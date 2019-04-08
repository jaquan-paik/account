from django.http import JsonResponse

from apps.domains.oauth2.constants import GrantType
from apps.domains.oauth2.serializers import AuthorizationCodeGrantSerializer, PasswordGrantSerializer, RefreshTokenGrantSerializer
from apps.domains.oauth2.services.oauth2_authorization_code_service import OAuth2AuthorizationCodeService
from apps.domains.oauth2.services.oauth2_password_service import OAuth2PasswordTokenService
from apps.domains.oauth2.services.oauth2_refresh_token_service import OAuth2RefreshTokenService


class OAuth2TokenServiceFactory:
    def __init__(self, grant_type: str, data: dict):
        self.grant_type = grant_type
        self._set_serializer_and_service(data)

    def _set_serializer_and_service(self, data):
        if self.grant_type == GrantType.AUTHORIZATION_CODE:
            self._serializer = AuthorizationCodeGrantSerializer(data=data)
            self._service = OAuth2AuthorizationCodeService
            return

        if self.grant_type == GrantType.PASSWORD:
            self._serializer = PasswordGrantSerializer(data=data)
            self._service = OAuth2PasswordTokenService
            return

        if self.grant_type == GrantType.REFRESH_TOKEN:
            self._serializer = RefreshTokenGrantSerializer(data=data)
            self._service = OAuth2RefreshTokenService
            return

    def get_tokens(self):
        return JsonResponse(self._service.get_tokens(**self._serializer.validated_data))

    def is_serializer_valid(self):
        return self._serializer.is_valid()

    def get_serializer_errors(self):
        return self._serializer.errors
