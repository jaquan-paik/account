from typing import Tuple

import requests
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from oauth2_provider.models import AbstractApplication
from oauth2_provider.settings import oauth2_settings

from apps.domains.callback.dtos import OAuth2Data, TokenData
from apps.domains.oauth2.models import Application
from infra.configure.config import GeneralConfig


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
        url = reverse('oauth2_provider:token')
        req = requests.post(f'https://{GeneralConfig.get_site_domain()}{url}', data={
            'client_id': client.client_id,
            'code': code,
            'redirect_uri': f'https://{GeneralConfig.get_site_domain()}{reverse("callback:callback")}',
            'client_secret': client.client_secret,
            'grant_type': 'authorization_code',
            'state': state,
        }, verify=False)  # TODO: 개발 완료되고 인증서 추가되면 verify 제거

        json = req.json()
        cls._validate_response(json, state)

        return cls._generate_token_from_json(json)

    @classmethod
    def get_tokens(cls, oauth2_data: OAuth2Data) -> Tuple[TokenData, TokenData]:
        client = Application.objects.get(client_id=oauth2_data.client_id)

        #  Authorization code 방식만 구현됨
        if client.authorization_grant_type != AbstractApplication.GRANT_AUTHORIZATION_CODE:
            raise NotImplementedError()

        return cls._take_token(client, oauth2_data.code, oauth2_data.state)
