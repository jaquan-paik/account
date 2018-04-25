from typing import Dict

from lib.ridibooks.api.store import StoreApi


class AccountInfoService:
    @staticmethod
    def get_account_info(access_token: str) -> Dict:
        api = StoreApi(access_token=access_token)
        return api.get_account_info()
