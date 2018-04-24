from json import JSONDecodeError
from typing import Dict, Optional

import requests
from requests import RequestException, Response

from infra.network.constants.http_status_code import HttpStatusCodes
from lib.ridibooks.api.domain import ApiDomain
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, HttpMethod
from lib.ridibooks.common.exceptions import InvalidResponseException, RequestFailException


class BaseApi:
    domain = None  # type: ApiDomain

    def __init__(self, access_token: str):
        self.access_token = access_token

    def _request(self, method: int, path: str, data: Optional[Dict]=None) -> Dict:
        kwargs = {
            'method': HttpMethod.to_string(method),
            'url': self._make_url(path=path),
            'cookies': self._make_cookies()
        }

        if method == HttpMethod.GET:
            kwargs['params'] = data
        else:
            kwargs['data'] = data

        try:
            response = requests.request(**kwargs)
        except RequestException as e:
            raise RequestFailException(e.response.status_code)

        return self._process_response(response=response)

    def _process_response(self, response: Response) -> Dict:
        if response.status_code != HttpStatusCodes.C_200_OK:
            raise RequestFailException(response.status_code)

        try:
            return response.json()
        except (JSONDecodeError, TypeError):
            raise InvalidResponseException(response.content)

    def _make_url(self, path: str) -> str:
        return f'{self.domain}{path}'

    def _make_cookies(self) -> Dict:
        return {
            ACCESS_TOKEN_COOKIE_KEY: self.access_token
        }
