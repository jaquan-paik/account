from datetime import datetime
from django.core.exceptions import PermissionDenied


class StateHelper:
    @staticmethod
    def create_encrypted_state(u_idx: str) -> str:
        return f"{datetime.now()}:{u_idx}"

    @staticmethod
    def _decrypt_state(state: str) -> dict:
        return {}

    @classmethod
    def validate_state(cls, state: str, u_idx: str):
        decrypted_state = cls._decrypt_state(state)
        print(decrypted_state)
        # check date, and u_id
        raise PermissionDenied()
