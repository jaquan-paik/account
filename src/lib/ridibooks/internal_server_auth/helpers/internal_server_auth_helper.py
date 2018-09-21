from datetime import datetime, timedelta
from json import JSONDecodeError
from typing import Tuple

import jwt
from jwt import DecodeError, InvalidTokenError
from jwt.exceptions import InvalidKeyError

from lib.ridibooks.internal_server_auth import settings
from lib.ridibooks.internal_server_auth.constants import DEFAULT_EXPIRE_MARGIN_MINS
from lib.ridibooks.internal_server_auth.helpers.config_helper import Config
from lib.ridibooks.internal_server_auth.utils import ConfigKeyMaker


class InternalServerAuthHelper:
    _ISSUER = 'iss'
    _SUBJECT = 'sub'
    _AUDIENCE = 'aud'
    _EXPIRE = 'exp'

    @classmethod
    def generate(cls, key: str) -> str:
        config = cls._get_config(key)
        payload = {
            cls._ISSUER: config.issuer,
            cls._AUDIENCE: config.audience,
            cls._EXPIRE: cls._get_expire(),
        }

        return jwt.encode(payload, config.secret, algorithm=config.alg).decode()

    @classmethod
    def verify(cls, token: str) -> bool:
        try:
            issuer, _, audience = cls._parse_token(token)
            config = cls._get_res_config(issuer, audience)

        except (KeyError, JSONDecodeError):
            return False

        try:
            jwt.decode(jwt=token, key=config.secret, algorithms=[config.alg], audience=config.audience, options={
                'require_exp': settings.RIDI_INTERNAL_AUTH_REQUIRE_EXP
            })

        except (InvalidTokenError, DecodeError, InvalidKeyError):
            return False

        return True

    @classmethod
    def _parse_token(cls, token: str) -> Tuple[str, str, str]:
        payload = jwt.decode(jwt=token, verify=False)

        subject = None
        if cls._SUBJECT in payload:
            subject = payload[cls._SUBJECT]

        return payload[cls._ISSUER], subject, payload[cls._AUDIENCE]

    @classmethod
    def _get_res_config(cls, issuer: str, audience: str) -> Config:
        key = ConfigKeyMaker.make_res_key(issuer, audience)
        return cls._get_config(key)

    @staticmethod
    def _get_config(key: str) -> Config:
        return settings.RIDI_INTERNAL_AUTH_DATA[key]

    @staticmethod
    def _get_expire() -> datetime:
        return datetime.now() + timedelta(minutes=DEFAULT_EXPIRE_MARGIN_MINS)
