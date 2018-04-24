from json import JSONDecodeError
from typing import Tuple

import jwt
from jwt import DecodeError, InvalidTokenError
from jwt.exceptions import InvalidKeyError

from lib.ridibooks.internal_server_auth import config
from lib.ridibooks.internal_server_auth.utils import make_auth_data_key


class JwtAuthHelper:
    @staticmethod
    def verify(token: str) -> bool:
        try:
            iss, sub = _get_iss_and_sub(token=token)
            secret, alg = _get_secret_and_alg(issuer=iss, subject=sub)
        except (KeyError, JSONDecodeError):
            return False

        try:
            payload = jwt.decode(jwt=token, key=secret, algorithms=[alg])

            if payload.get('iss') != iss or payload.get('sub') != sub:
                return False
        except (InvalidTokenError, DecodeError, InvalidKeyError):
            return False

        return True


def _get_iss_and_sub(token: str) -> Tuple[str, str]:
    payload = jwt.decode(jwt=token, verify=False)
    return payload['iss'], payload['sub']


def _get_secret_and_alg(issuer: str, subject: str) -> Tuple[str, str]:
    key = make_auth_data_key(issuer=issuer, subject=subject)
    return config.RIDI_INTERNAL_AUTH_DATA[key]
