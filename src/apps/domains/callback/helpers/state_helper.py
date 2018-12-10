from datetime import datetime
from django.core.exceptions import PermissionDenied

from infra.configure.constants import SecretKeyName
from lib.secret.secret import Secret
from lib.crypto.encrypt import CryptoHelper
import json

CRYPTO_KEY = Secret().get(SecretKeyName.SECRET_KEY)[:32]
EXPIRE_TIME = 10


class StateHelper:
    @staticmethod
    def create_encrypted_state(u_idx: str) -> str:
        state = {'time': datetime.now().timestamp(), 'u_idx': u_idx}
        return CryptoHelper(CRYPTO_KEY).encrypt(json.dumps(state))

    @staticmethod
    def _decrypt_state(state: str) -> dict:
        decrypted_data = json.loads(CryptoHelper(CRYPTO_KEY).decrypt(state))
        if not decrypted_data:
            raise PermissionDenied()
        return decrypted_data

    @classmethod
    def validate_state(cls, state: str, u_idx: str):
        decrypted_data = cls._decrypt_state(state)
        if decrypted_data['u_idx'] != u_idx:
            raise PermissionDenied()
        if decrypted_data['time'] + EXPIRE_TIME < datetime.now().timestamp():
            raise PermissionDenied()
