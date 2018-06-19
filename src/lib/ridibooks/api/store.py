from typing import Dict, Optional

from lib.ridibooks.api.base import ApiDomain, BaseApi
from lib.ridibooks.common.constants import HttpMethod

DEV_RIDI_STORE_DOMAIN = 'https://dev.ridi.io'
DEV_RIDI_COM_STORE_DOMAIN = 'http://login.dev.ridi.com'
PROD_RIDI_STORE_DOMAIN = 'https://ridibooks.com'


class StoreApi(BaseApi):
    domain = ApiDomain(dev=DEV_RIDI_STORE_DOMAIN, prod=PROD_RIDI_STORE_DOMAIN)

    ACCOUNT_INFO = '/api/account/info'

    def __init__(self, access_token: Optional[str] = None, phpsession_id: Optional[str] = None, is_ridi_com: bool = False):
        super().__init__(access_token, phpsession_id)

        if is_ridi_com:
            self.domain = DEV_RIDI_COM_STORE_DOMAIN

    def get_account_info(self) -> Dict:
        return self._request(method=HttpMethod.GET, path=self.ACCOUNT_INFO)
