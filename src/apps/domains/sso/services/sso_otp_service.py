import json
from datetime import datetime, timedelta
from typing import Tuple

from dateutil import parser

from apps.domains.sso.constants import SSO_TOKEN_TTL
from apps.domains.sso.exceptions import FailVerifyOtpException
from lib.crypto.encrypt import CryptoHelper


class SSOOtpService:
    @staticmethod
    def generate(key: str, u_idx: int, client_id: str = None, ttl: int = SSO_TOKEN_TTL) -> str:
        expire_date = datetime.now() + timedelta(seconds=ttl)
        data = {
            'u_idx': u_idx,
            'expire_date': str(expire_date)
        }

        if client_id:
            data['client_id'] = client_id

        return CryptoHelper(key).encrypt(json.dumps(data))

    @staticmethod
    def verify(key: str, otp: str) -> Tuple[int, str]:
        try:
            body = CryptoHelper(key).decrypt(otp)
            data = json.loads(body)
        except Exception:
            raise FailVerifyOtpException('복호화에 실패했습니다.')

        now = datetime.now()
        expire_date = parser.parse(data['expire_date'])
        if now > expire_date:
            raise FailVerifyOtpException('토큰 유효시간이 만료되었습니다.')

        return data['u_idx'], data['client_id']
