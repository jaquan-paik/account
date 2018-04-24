import requests
from requests import RequestException

from infra.network.constants.http_status_code import HttpStatusCodes
from lib.ridibooks.common.exceptions import InvalidResponseException, NotEnoughArgumentsException, ServerException
from lib.ridibooks.php_auth.api_url import RidiStoreApiUrl


class RidiApiHelper:
    def __init__(self, phpsession_id: str=None):
        self.phpsession_id = phpsession_id

    def get_account_info(self):
        if self.phpsession_id is None:
            raise NotEnoughArgumentsException

        cookies = dict(PHPSESSID=self.phpsession_id)

        try:
            response = requests.get(RidiStoreApiUrl.get_url(RidiStoreApiUrl.ACCOUNT_INFO), cookies=cookies)
        except RequestException:
            raise ServerException

        if response.status_code != HttpStatusCodes.C_200_OK:
            raise ServerException(response.status_code)

        try:
            account_info = response.json()
        except ValueError:
            raise InvalidResponseException(response.content)

        return account_info
