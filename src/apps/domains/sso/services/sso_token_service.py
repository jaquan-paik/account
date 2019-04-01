import json
from datetime import datetime, timedelta

from dateutil import parser

from apps.domains.sso.exceptions import FailVerifyTokenException
from lib.crypto.encrypt import CryptoHelper


class SSOTokenService:
    @staticmethod
    def generate(u_idx: int, ttl: int, key: str) -> str:
        expire_date = datetime.now() + timedelta(seconds=ttl)

        data = {
            'u_idx': u_idx,
            'expire_date': str(expire_date)
        }

        return CryptoHelper(key).encrypt(json.dumps(data))

    @staticmethod
    def verify(token: str, key: str) -> int:
        try:
            body = CryptoHelper(key).decrypt(token)
            data = json.loads(body)
        except Exception:
            raise FailVerifyTokenException('복호화에 실패했습니다.')

        now = datetime.now()
        expire_date = parser.parse(data['expire_date'])
        if now > expire_date:
            raise FailVerifyTokenException('토큰 유효시간이 만료되었습니다.')

        return data['u_idx']
