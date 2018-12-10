from datetime import datetime
from django.core.exceptions import PermissionDenied

from infra.configure.constants import SecretKeyName
from lib.secret.secret import Secret
from lib.crypto.encrypt import CryptoHelper
import json

CRYPTO_KEY = '!Ck[v%W}$5,4@-5R'


class StateHelper:
    @staticmethod
    def create_encrypted_state(u_idx: str) -> str:
        state = {'datetime': str(datetime.now()), 'u_idx': u_idx}
        # return CryptoHelper(Secret().get(SecretKeyName.SECRET_KEY)).encrypt(json.dumps(state))
        return CryptoHelper(CRYPTO_KEY).encrypt(json.dumps(state))

    @staticmethod
    def _decrypt_state(state: str) -> str:
        return CryptoHelper(CRYPTO_KEY).decrypt(state)

    @classmethod
    def validate_state(cls, state: str, u_idx: str):
        decrypted_state = cls._decrypt_state(state)
        from lib.log.logger import logger
        logger.info(decrypted_state)
        # raise PermissionDenied()
