from datetime import datetime

import jwt

from apps.domains.account.models import User
from apps.domains.oauth2.constants import ACCESS_TOKEN_EXPIRE_SECONDS, JwtAlg
from apps.domains.oauth2.models import Application


class AccessTokenService:
    @staticmethod
    def generate(client: Application, user: User, scope: str) -> str:
        payload = {
            'sub': user.id,
            'exp': round(datetime.now().timestamp()) + ACCESS_TOKEN_EXPIRE_SECONDS,
            'u_idx': user.idx,
            'client_id': client.id,
            'scope': scope
        }

        return jwt.encode(payload, client.jwt_hs_256_secret, algorithm=JwtAlg.HS256).decode()
