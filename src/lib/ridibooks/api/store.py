import json
from typing import Dict

from infra.configure.config import GeneralConfig
from lib.log.logger import logger
from lib.ridibooks.api.base import BaseApi
from lib.ridibooks.api.exceptions import InvalidRequestException, InvalidUserDormantedException, InvalidUserNotFoundException, \
    InvalidUserSecededException, InvalidUserUnauthorizedException, InvalidUserUnmatchedPasswordException, InvalidUserUnverifiedException, \
    StoreInternalServerErrorException
from lib.ridibooks.common.constants import HttpMethod
from lib.ridibooks.common.exceptions import HTTPException
from lib.ridibooks.internal_server_auth.constants import AuthList


class StoreApi(BaseApi):
    domain = GeneralConfig.get_store_url()

    ACCOUNT_INFO = '/api/account/info'
    IS_LOGINABLE = '/api/account/is-loginable'

    def get_account_info(self) -> Dict:
        return self._request(method=HttpMethod.GET, path=self.ACCOUNT_INFO)

    def is_loginable(self, username: str, password: str) -> Dict:
        try:
            return self._request_with_internal_server_auth(
                token_key=AuthList.ACCOUNT_TO_STORE,
                method=HttpMethod.POST, path=self.IS_LOGINABLE, data={'u_id': username, 'password': password}, is_json_data=True
            )

        except HTTPException as e:
            content = json.loads(e.content.decode('utf-8'))
            if e.status == 400:
                logger.error(f'[STORE API][IS_LOGINABLE] Error: {content}')
                raise InvalidRequestException()

            elif e.status == 401:
                if content['code'] == 'UNAUTHORIZED':
                    raise InvalidUserUnauthorizedException()
                elif content['code'] == 'UNVERIFIED_ACCOUNT':
                    raise InvalidUserUnverifiedException()
                elif content['code'] == 'SECEDED_ACCOUNT':
                    raise InvalidUserSecededException()
                elif content['code'] == 'DORMANTED_ACCOUNT':
                    raise InvalidUserDormantedException()
                elif content['code'] == 'UNMATCHED_PASSWORD':
                    raise InvalidUserUnmatchedPasswordException()

            elif e.status == 404:
                if content['code'] == 'ACCOUNT_NOT_FOUND':
                    raise InvalidUserNotFoundException()

            elif e.status == 500:
                raise StoreInternalServerErrorException()

            logger.error(f'[STORE API][IS_LOGINABLE] Error: {e.status} - {content}')
            raise NotImplementedError()
