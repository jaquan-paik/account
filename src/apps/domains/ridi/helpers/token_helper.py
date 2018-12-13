from datetime import datetime
from oauth2_provider.oauth2_validators import AccessToken

from apps.domains.ridi.dtos import TokenData


class TokenHelper:

    @staticmethod
    def get_token_data_info(token_data: TokenData) -> dict:
        return {
            'expires_at': token_data.expires_at,
            'expires_in': token_data.expires_in
        }

    @staticmethod
    def get_token_info(access_token: AccessToken) -> dict:
        return {
            'expires_at': access_token.expires,
            'expires_in': int(access_token.expires - datetime.now().timestamp()),
        }
