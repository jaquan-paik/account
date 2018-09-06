from json import JSONDecodeError
from typing import Dict, Optional

import requests
from requests import Response
from requests.exceptions import HTTPError, RequestException

from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, HttpMethod, PHP_SESSION_COOKIE_KEY
from lib.ridibooks.common.exceptions import HTTPException, InvalidResponseException, ServerException
from lib.ridibooks.internal_server_auth.helpers.internal_server_auth_helper import InternalServerAuthHelper
from lib.ridibooks.internal_server_auth.utils import TokenHandler


class BaseApi:
    domain = None

    def __init__(self, access_token: Optional[str] = None, phpsession_id: Optional[str] = None):
        self.access_token = access_token
        self.phpsession_id = phpsession_id

    def _request(
            self, method: int, path: str, headers: Optional[Dict] = None, data: Optional[Dict] = None, is_json_data: bool = False
    ) -> Dict:
        kwargs = {
            'method': HttpMethod.to_string(method),
            'url': self._make_url(path=path),
            'headers': headers,
            'cookies': self._make_cookies(),
            'timeout': 60,
        }

        if method == HttpMethod.GET:
            kwargs['params'] = data

        else:
            if is_json_data:
                kwargs['data'] = data
            else:
                kwargs['json'] = data

        try:
            response = requests.request(**kwargs)
        except RequestException:
            raise ServerException()

        return self._process_response(response=response)

    def _request_with_internal_server_auth(
            self, token_key: str, method: int, path: str, data: Optional[Dict] = None, is_json_data: bool = False
    ):
        headers = {
            'Authorization': TokenHandler.make(InternalServerAuthHelper.generate(token_key)),
        }

        return self._request(method, path, headers, data, is_json_data)

    def _process_response(self, response: Response) -> Dict:
        try:
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            raise HTTPException(origin_exception=e, content=e.response.content, status=e.response.status_code)
        except (JSONDecodeError, TypeError):
            raise InvalidResponseException(response.content)

    def _make_url(self, path: str) -> str:
        return f'{self.domain}{path}'

    def _make_cookies(self) -> Dict:
        _cookies = {}

        if self.access_token:
            _cookies[ACCESS_TOKEN_COOKIE_KEY] = self.access_token

        if self.phpsession_id:
            _cookies[PHP_SESSION_COOKIE_KEY] = self.phpsession_id

        return _cookies
