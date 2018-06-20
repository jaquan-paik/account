from typing import Dict, Optional

from infra.configure.config import GeneralConfig
from lib.ridibooks.api.base import BaseApi
from lib.ridibooks.common.constants import HttpMethod


class StoreApi(BaseApi):
    domain = GeneralConfig.get_store_url()

    ACCOUNT_INFO = '/api/account/info'

    def get_account_info(self) -> Dict:
        return self._request(method=HttpMethod.GET, path=self.ACCOUNT_INFO)
