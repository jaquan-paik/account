from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from oauth2_provider.oauth2_validators import RefreshToken

from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.token_request_helper import TokenRequestHelper


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
        return TokenRequestHelper.get_tokens(grant_type='refresh_token', client=client, refresh_token=refresh_token)
