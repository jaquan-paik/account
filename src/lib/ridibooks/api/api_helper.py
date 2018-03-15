import requests
from requests import RequestException

from infra.network.constants.http_status_code import HttpStatusCodes
from lib.ridibooks.api.api_url import RidiStoreApiUrl
from lib.ridibooks.exceptions import InvalidResponseException, NotEnoughArgumentsException, RequestFailException


class RidiApiHelper:
    def __init__(self, phpsession_id: str=None):
        self.phpsession_id = phpsession_id

    def get_account_info(self):
        if self.phpsession_id is None:
            raise NotEnoughArgumentsException

        cookies = dict(PHPSESSID=self.phpsession_id)

        try:
            response = requests.get(RidiStoreApiUrl.get_url(RidiStoreApiUrl.ACCOUNT_INFO), cookies=cookies, verify=False)
            # ssl인증서가 만료되었기떄문에 verify옵션을 False로주고 테스트한다.
        except RequestException:
            raise RequestFailException

        if response.status_code != HttpStatusCodes.C_200_OK:
            raise RequestFailException(response.status_code)

        try:
            account_info = response.json()
        except ValueError:
            raise InvalidResponseException(response.content)

        return account_info
