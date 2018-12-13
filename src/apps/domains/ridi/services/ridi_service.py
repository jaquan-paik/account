from typing import Tuple
from datetime import datetime
from django.urls import reverse
from oauth2_provider.oauth2_validators import AccessToken

from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.client_helper import ClientHelper
from apps.domains.ridi.helpers.state_helper import StateHelper
from apps.domains.ridi.helpers.token_request_helper import TokenRequestHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper

from lib.utils.url import generate_query_url


class RidiService:
    @staticmethod
    def get_oauth2_authorize_url(client_id: str, redirect_uri: str, u_idx: str) -> str:
        params = {
            'client_id': client_id,
            'redirect_uri': UrlHelper.get_redirect_url(redirect_uri, client_id),
            'response_type': 'code',
            'state': StateHelper.create_encrypted_state(u_idx),
        }
        url = generate_query_url(reverse('oauth2_provider:authorize'), params)
        return url

    @staticmethod
    def get_token(code: str, client_id: str, in_house_redirect_uri: str) -> Tuple[TokenData, TokenData]:
        access_token, refresh_token = TokenRequestHelper.get_tokens(
            grant_type='authorization_code', client=ClientHelper.get_in_house_client(client_id),
            code=code, redirect_uri=UrlHelper.get_redirect_url(in_house_redirect_uri, client_id)
        )
        return access_token, refresh_token

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
