from typing import Dict

from lib.ridibooks.api.base import ApiDomain, BaseApi
from lib.ridibooks.common.constants import HttpMethod

DEV_RIDI_STORE_DOMAIN = 'https://dev.ridi.io'
PROD_RIDI_STORE_DOMAIN = 'https://ridibooks.com'


class StoreApi(BaseApi):
    domain = ApiDomain(dev=DEV_RIDI_STORE_DOMAIN, prod=PROD_RIDI_STORE_DOMAIN)

    ACCOUNT_INFO = '/api/account/info'

    def get_account_info(self) -> Dict:
        return self._request(method=HttpMethod.GET, path=self.ACCOUNT_INFO)
