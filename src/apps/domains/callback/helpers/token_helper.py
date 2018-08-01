from typing import Tuple

import requests
from django.core.exceptions import PermissionDenied

from apps.domains.callback.dtos import TokenData
from apps.domains.callback.helpers.url_helper import UrlHelper
from apps.domains.oauth2.models import Application
from infra.configure.config import GeneralConfig


class TokenHelper:
    @staticmethod
    def _validate_response(json: dict, state: str) -> None:
        if json.get('state', None) != state:
            raise PermissionDenied()

    @staticmethod
    def _generate_token_from_json(response_json: dict) -> Tuple[TokenData, TokenData]:
        access_token = response_json.get('access_token', None)
        access_token_expires_in = response_json.get('expires_in', None)

        refresh_token = response_json.get('refresh_token', None)
        refresh_token_expire_in = response_json.get('refresh_token_expires_in', None)

        return TokenData(access_token, access_token_expires_in), TokenData(refresh_token, refresh_token_expire_in)

    @classmethod
    def _take_token(cls, client: Application, code: str, state: str) -> Tuple[TokenData, TokenData]:
        verify = not GeneralConfig.is_dev()
        req = requests.post(
            UrlHelper.get_token(), data=cls._get_request_data(client, code, state), verify=verify,
        )
        req.raise_for_status()

        json = req.json()
        cls._validate_response(json, state)
        return cls._generate_token_from_json(json)

    @classmethod
    def get_tokens(cls, client: Application, code: str, state: str=None) -> Tuple[TokenData, TokenData]:
        return cls._take_token(client, code, state)

    @staticmethod
    def _get_request_data(client: Application, code: str, state: str):
        raise NotImplementedError()

    @staticmethod
    def _get_default_request_data(client: Application):
        return {
            'client_id': client.client_id,
            'redirect_uri': UrlHelper.get_redirect_uri(),
            'client_secret': client.client_secret,
        }


class TokenCodeHelper(TokenHelper):
    @classmethod
    def _get_request_data(cls, client: Application, code: str, state: str) -> dict:
        data = cls._get_default_request_data(client)
        data['code'] = code
        data['grant_type'] = 'authorization_code'

        if state is not None:
            data['state'] = state

        return data


class TokenRefreshHelper(TokenHelper):
    @classmethod
    def _get_request_data(cls, client: Application, refresh_token: str, state: str):
        data = cls._get_default_request_data(client)
        data['refresh_token'] = refresh_token
        data['grant_type'] = 'refresh_token'

        return data
