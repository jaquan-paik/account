from typing import Dict, Tuple

from lib.ridibooks.internal_server_auth.config import Config
from lib.ridibooks.internal_server_auth.constants import AuthList, DEFAULT_ALG
from lib.ridibooks.internal_server_auth.utils import ConfigKeyMaker


class ConfigHelper:
    @classmethod
    def generate_auth_data(cls, secret_keys: Dict) -> Dict[str, Config]:
        config = {}
        for auth in AuthList.get_list():
            if auth not in secret_keys:
                continue

            secret = secret_keys[auth]
            issuer, audience = cls._parse_auth_data(auth)

            if auth != ConfigKeyMaker.make_req_key(issuer, audience):
                raise KeyError('Fail key generate.')

            config[auth] = Config(cls._decode_secret(secret), DEFAULT_ALG, issuer, audience)

        return config

    @staticmethod
    def _parse_auth_data(auth: str) -> Tuple[str, str]:
        split_auth = auth.split(':')
        issuer = split_auth[0]
        audience = split_auth[1]

        return issuer, audience

    @staticmethod
    def _decode_secret(secret: str) -> str:
        return bytes(secret, 'utf-8').decode('unicode_escape')
