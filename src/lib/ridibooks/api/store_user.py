from datetime import datetime
from typing import Dict, List

from infra.configure.config import GeneralConfig
from lib.decorators.alarm import LogExecuteKey, log_execute_time
from lib.ridibooks.api.base import BaseApi
from lib.ridibooks.common.constants import HttpMethod
from lib.ridibooks.internal_server_auth.constants import AuthList


class StoreUserApi(BaseApi):
    domain = GeneralConfig.get_store_api_url()

    SYNC_UPDATED_USERS = '/sync/updated-users'
    SYNC_USERS = '/sync/users'

    def get_updated_user_idxes_by_before(self, before: datetime) -> Dict:
        return log_execute_time(LogExecuteKey.STORE_API_ACCOUNT_UPDATED_USERS, timeout=30, always=False, with_sentry_if_exceeded=True)(
            self._request_with_internal_server_auth
        )(
            token_key=AuthList.ACCOUNT_TO_STORE, method=HttpMethod.GET, path=self.SYNC_UPDATED_USERS,
            data={'before': before.isoformat()}, is_json_data=True
        )

    def get_users_by_idxes(self, user_idxes: List[int]) -> List:
        return log_execute_time(LogExecuteKey.STORE_API_ACCOUNT_USERS, timeout=30, always=False, with_sentry_if_exceeded=True)(
            self._request_with_internal_server_auth
        )(
            token_key=AuthList.ACCOUNT_TO_STORE, method=HttpMethod.GET, path=self.SYNC_USERS,
            data={'u_idx[]': user_idxes}, is_json_data=True
        )
