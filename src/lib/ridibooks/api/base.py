from json import JSONDecodeError
from typing import Dict, Optional

import requests
from requests import Response
from requests.exceptions import HTTPError, RequestException

from lib.ridibooks.api.domain import ApiDomain
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, HttpMethod, PHP_SESSION_COOKIE_KEY
from lib.ridibooks.common.exceptions import HTTPException, InvalidResponseException, ServerException


class BaseApi:
    domain = None  # type: ApiDomain

    def __init__(self, access_token: Optional[str]=None, phpsession_id: Optional[str]=None):
        self.access_token = access_token
        self.phpsession_id = phpsession_id

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
        except RequestException:
            raise ServerException()

        return self._process_response(response=response)

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
