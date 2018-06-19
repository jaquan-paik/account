from typing import Dict

from apps.domains.callback.constants import CookieRootDomains
from lib.ridibooks.api.store import StoreApi


class AccountInfoService:
    @classmethod
    def get_account_info(cls, host: str, access_token: str) -> Dict:
        return StoreApi(access_token=access_token, is_ridi_com=cls.is_dev_ridi_com(host)).get_account_info()

    @classmethod
    def get_account_info_by_ridibooks_session_id(cls, host: str, ridibooks_session_id: str) -> Dict:
        return StoreApi(phpsession_id=ridibooks_session_id, is_ridi_com=cls.is_dev_ridi_com(host)).get_account_info()

    @staticmethod
    def is_dev_ridi_com(host: str) -> bool:
        return host.find(CookieRootDomains.to_string(CookieRootDomains.DEV_RIDI_COM)) > 0
