from typing import Dict, Tuple

from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.http import Http404
from oauthlib.oauth2 import OAuth2Error

from apps.domains.oauth2.models import Application as Client
from apps.domains.oauth2.services.oauth2_authorization_code_service import OAuth2AuthorizationCodeService
from apps.domains.oauth2.services.oauth2_refresh_token_service import OAuth2RefreshTokenService
from apps.domains.ridi.dtos import TokenData
from infra.network.constants.http_status_code import HttpStatusCodes


class Oauth2TokenHelper:
    @classmethod
    def get_tokens_data_by_authorization_code_grant(cls, client: Client, code: str, redirect_uri: str) -> Tuple[TokenData, TokenData]:
        try:
            tokens = OAuth2AuthorizationCodeService.get_tokens(client.client_id, client.client_secret, code, redirect_uri)
            return cls._get_tokens_data(tokens)

        except OAuth2Error as error:
            if error.status_code == HttpStatusCodes.C_400_BAD_REQUEST:
                raise SuspiciousOperation
            if error.status_code == HttpStatusCodes.C_403_FORBIDDEN:
                raise PermissionDenied
            if error.status_code == HttpStatusCodes.C_404_NOT_FOUND:
                raise Http404
            raise error

    @classmethod
    def get_tokens_data_by_refresh_token(cls, client: Client, refresh_token: str) -> Tuple[TokenData, TokenData]:
        try:
            tokens = OAuth2RefreshTokenService.get_tokens(client.client_id, client.client_secret, refresh_token)
            return cls._get_tokens_data(tokens)

        except OAuth2Error as error:
            if error.status_code == HttpStatusCodes.C_400_BAD_REQUEST:
                raise SuspiciousOperation
            if error.status_code == HttpStatusCodes.C_403_FORBIDDEN:
                raise PermissionDenied
            if error.status_code == HttpStatusCodes.C_404_NOT_FOUND:
                raise Http404
            raise error

    @staticmethod
    def _get_tokens_data(tokens: Dict) -> Tuple[TokenData, TokenData]:
        access_token = tokens.get('access_token')
        access_token_expires_in = tokens.get('expires_in')
        refresh_token = tokens.get('refresh_token')
        refresh_token_expires_in = tokens.get('refresh_token_expires_in')
        return TokenData(access_token, access_token_expires_in), TokenData(refresh_token, refresh_token_expires_in)
