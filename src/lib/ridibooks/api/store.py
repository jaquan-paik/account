from typing import Dict

from infra.configure.config import GeneralConfig
from lib.ridibooks.api.base import BaseApi
from lib.ridibooks.common.constants import HttpMethod
from lib.ridibooks.internal_server_auth.constants import AuthList


class StoreApi(BaseApi):
    domain = GeneralConfig.get_store_url()

    ACCOUNT_INFO = '/api/account/info'
    IS_LOGINABLE = '/api/account/is-loginable'

    def get_account_info(self) -> Dict:
        return self._request(method=HttpMethod.GET, path=self.ACCOUNT_INFO)

    def is_loginable(self, username: str, password: str) -> Dict:
        return self._request_with_internal_server_auth(
            token_key=AuthList.ACCOUNT_TO_STORE,
            method=HttpMethod.POST, path=self.IS_LOGINABLE, data={'u_id': username, 'password': password}, is_json_data=True
        )
