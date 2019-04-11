from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from oauth2_provider.oauth2_validators import RefreshToken

from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.oauth2_token_helper import OAuth2TokenHelper


class TokenRefreshService:
    @staticmethod
    def get_tokens(refresh_token: str) -> Tuple[TokenData, TokenData]:
        try:
            refresh_token = RefreshToken.objects.select_related('application').get(token=refresh_token)
        except ObjectDoesNotExist:
            raise PermissionDenied()

        client = refresh_token.application
        if not client.is_in_house:
            raise PermissionDenied()

        return OAuth2TokenHelper.get_tokens_data_by_refresh_token(client, refresh_token.token)
