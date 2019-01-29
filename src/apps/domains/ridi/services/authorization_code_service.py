from typing import Tuple

from django.urls import reverse

from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.client_helper import ClientHelper
from apps.domains.ridi.helpers.state_helper import StateHelper
from apps.domains.ridi.helpers.token_request_helper import TokenRequestHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper
from apps.domains.oauth2.constants import GrantType
from lib.utils.url import generate_query_url


class AuthorizationCodeService:
    @staticmethod
    def _validate_client_and_redirect_uri(client_id: str, redirect_uri: str):
        client = ClientHelper.get_in_house_client(client_id)
        ClientHelper.assert_in_house_client_redirect_uri(client, redirect_uri)

    @staticmethod
    def get_tokens(code: str, client_id: str, in_house_redirect_uri: str) -> Tuple[TokenData, TokenData]:
        access_token, refresh_token = TokenRequestHelper.get_tokens(
            grant_type=GrantType.AUTHORIZATION_CODE, client=ClientHelper.get_in_house_client(client_id),
            code=code, redirect_uri=UrlHelper.get_redirect_url(in_house_redirect_uri, client_id)
        )
        return access_token, refresh_token

    @classmethod
    def get_oauth2_authorize_url(cls, client_id: str, redirect_uri: str, u_idx: str) -> str:
        cls._validate_client_and_redirect_uri(client_id, redirect_uri)
        params = {
            'client_id': client_id,
            'redirect_uri': UrlHelper.get_redirect_url(redirect_uri, client_id),
            'response_type': 'code',
            'state': StateHelper.create_encrypted_state(u_idx),
        }
        url = generate_query_url(reverse('oauth2_provider:authorize'), params)
        return url
