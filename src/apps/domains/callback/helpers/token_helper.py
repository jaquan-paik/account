from typing import Tuple

import requests
from django.core.exceptions import PermissionDenied
from oauth2_provider.settings import oauth2_settings

from apps.domains.callback.dtos import OAuth2Data, TokenData
from apps.domains.callback.helpers.url_helper import UrlHelper
from apps.domains.oauth2.models import Application


class TokenHelper:
    @classmethod
    def _validate_response(cls, json: dict, state: str) -> None:
        if json.get('state', None) != state:
            raise PermissionDenied()

    @classmethod
    def _generate_token_from_json(cls, response_json: dict) -> Tuple[TokenData, TokenData]:
        access_token = response_json.get('access_token', None)
        access_token_expires_in = response_json.get('expires_in', None)

        refresh_token = response_json.get('refresh_token', None)
        refresh_token_expire_in = oauth2_settings.REFRESH_TOKEN_EXPIRE_SECONDS

        return TokenData(access_token, access_token_expires_in), TokenData(refresh_token, refresh_token_expire_in)

    @classmethod
    def _take_token(cls, client: Application, code: str, state: str) -> Tuple[TokenData, TokenData]:
        req = requests.post(UrlHelper.get_token(), data={
            'client_id': client.client_id,
            'code': code,
            'redirect_uri': UrlHelper.get_redirect_uri(),
            'client_secret': client.client_secret,
            'grant_type': 'authorization_code',
            'state': state,
        }, verify=False)  # TODO: 개발 완료되고 인증서 추가되면 verify 제거

        json = req.json()
        cls._validate_response(json, state)

        return cls._generate_token_from_json(json)

    @classmethod
    def get_tokens(cls, oauth2_data: OAuth2Data) -> Tuple[TokenData, TokenData]:
        return cls._take_token(oauth2_data.client, oauth2_data.code, oauth2_data.state)
