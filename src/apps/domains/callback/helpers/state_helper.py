import binascii
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.conf import settings
from lib.crypto.encrypt import CryptoHelper
from lib.log.logger import logger
import json

CRYPTO_KEY = settings.STATE_CRYPTO_KEY
EXPIRE_TIME = 10


class StateHelper:
    @staticmethod
    def create_encrypted_state(u_idx: str) -> str:
        state = {'time': datetime.now().timestamp(), 'u_idx': u_idx}
        return CryptoHelper(CRYPTO_KEY).encrypt(json.dumps(state))

    @staticmethod
    def _decrypt_state(state: str) -> dict:
        try:
            decrypted_str = CryptoHelper(CRYPTO_KEY).decrypt(state)
        except binascii.Error:
            raise PermissionDenied()  # base 64 decode 시, padding 길이가 다를 때 발생
        except ValueError:
            raise PermissionDenied()  # cipher text 의 길이가 다를 때 발생
        if not decrypted_str:
            raise PermissionDenied()  # 복호화가 정상적으로 되지 않을 때 발생
        return json.loads(decrypted_str)

    @classmethod
    def validate_state(cls, state: str, u_idx: int):
        decrypted_data = cls._decrypt_state(state)
        if decrypted_data['u_idx'] != u_idx:
            raise PermissionDenied()
        if decrypted_data['time'] + EXPIRE_TIME < datetime.now().timestamp():
            logger.info('EXCEED_STATE_EXPIRE_TIME', extra={
                'u_idx': u_idx,
                'decrypted_time': decrypted_data['time'],
                'exceed_seconds': datetime.now().timestamp() - decrypted_data['time']
            })
            raise PermissionDenied()
