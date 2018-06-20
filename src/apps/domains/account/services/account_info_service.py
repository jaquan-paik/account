from typing import Dict

from lib.ridibooks.api.store import StoreApi


class AccountInfoService:
    @classmethod
    def get_account_info(cls, access_token: str) -> Dict:
        return StoreApi(access_token=access_token).get_account_info()
