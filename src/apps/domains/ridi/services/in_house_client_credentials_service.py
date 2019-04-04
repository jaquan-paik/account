from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from apps.domains.account.models import User
from apps.domains.oauth2.exceptions import DisallowedGrantType, FailOAuth2Exception
from apps.domains.oauth2.services.oauth2_client_credentials_service import OAuth2ClientCredentialsService
from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.client_helper import ClientHelper


class InHouseClientCredentialsService:
    @classmethod
    def get_tokens(cls, client_id: str, u_idx: int) -> Tuple[TokenData, TokenData]:
        try:
            client = ClientHelper.get_in_house_client(client_id)
            user = User.objects.get(idx=u_idx)
            tokens = OAuth2ClientCredentialsService.get_tokens(client.client_id, client.client_secret, user)
        except (PermissionDenied, ObjectDoesNotExist, DisallowedGrantType) as e:
            raise FailOAuth2Exception()

        access_token = TokenData(tokens['access_token'], tokens['expires_in'])
        refresh_token = TokenData(tokens['refresh_token'], tokens['refresh_token_expires_in'])

        return access_token, refresh_token
