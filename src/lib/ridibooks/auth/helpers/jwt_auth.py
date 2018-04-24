import base64
import json
from json import JSONDecodeError
from typing import Dict, Tuple

import jwt
from jwt import DecodeError, InvalidTokenError
from jwt.exceptions import InvalidKeyError

from lib.ridibooks.auth import config
from lib.ridibooks.auth.utils import make_auth_data_key


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
    payload_str = token.split('.')[1]
    payload = _load_payload(payload_str=payload_str)
    return payload['iss'], payload['sub']


def _get_secret_and_alg(issuer: str, subject: str) -> Tuple[str, str]:
    key = make_auth_data_key(issuer=issuer, subject=subject)
    return config.RIDI_INTERNAL_AUTH_DATA[key]


def _load_payload(payload_str: str) -> Dict:
    payload = json.loads(base64.b64decode(_add_padding(payload_str)))
    return payload


def _add_padding(b64str: str) -> bytes:
    pad_str = b64str + '=' * (-len(b64str) % 4)
    return pad_str.encode('utf-8')
