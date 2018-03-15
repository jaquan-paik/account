from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from oauth2_provider.oauth2_validators import RefreshToken

from apps.domains.callback.dtos import TokenData
from apps.domains.callback.helpers.token_helper import TokenRefreshHelper


class TokenRefreshService:
    @staticmethod
    def refresh(cookie_refresh_token: str) -> Tuple[TokenData, TokenData]:
        try:
            refresh_token = RefreshToken.objects.select_related('application').get(token=cookie_refresh_token)
        except ObjectDoesNotExist:
            raise PermissionDenied()

        client = refresh_token.application
        if not client.is_in_house:
            raise PermissionDenied()

        return TokenRefreshHelper.get_tokens(client.client_id, refresh_token)
