from datetime import datetime

import jwt
from oauth2_provider.oauth2_validators import AccessToken
from oauth2_provider.settings import oauth2_settings

from apps.domains.oauth2.constants import JWT_VERIFY_MARGIN, JwtAlg
from apps.domains.oauth2.exceptions import JwtTokenErrorException
from apps.domains.oauth2.models import Application


class JwtHandler:
    @staticmethod
    def _get_client_from_token(token: str):
        # JWT의 secret을 가져오기 위해 verify 을 하지 않고 decode를 한다.
        try:
            unverified_payload = jwt.decode(token, verify=False)
        except jwt.exceptions.InvalidTokenError:
            raise JwtTokenErrorException()
        return Application.objects.get(client_id=unverified_payload['client_id'])

    @staticmethod
    def generate(request, refresh_token=False):
        user = request.user
        client = request.client
        scopes = request.scopes

        payload = {
            'sub': user.id,
            'u_idx': user.idx,
            'exp': round(datetime.now().timestamp()) + oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            'client_id': client.client_id,
            'scope': ' '.join(scopes)
        }

        if client.jwt_alg == JwtAlg.HS256:
            return jwt.encode(payload, client.jwt_hs_256_secret, algorithm=JwtAlg.HS256).decode()

        raise NotImplementedError(f'Jwt alg is not implemented: {client.jwt_alg}')

    @classmethod
    def validate(cls, token: str, client: Application) -> dict:
        try:
            if client.jwt_alg == JwtAlg.HS256:
                return jwt.decode(token, key=client.jwt_hs_256_secret, algorithm=JwtAlg.HS256, leeway=JWT_VERIFY_MARGIN)
        except jwt.exceptions.InvalidTokenError:
            raise JwtTokenErrorException()

        raise NotImplementedError(f'Jwt alg is not implemented: {client.jwt_alg}')

    @classmethod
    def get_access_token(cls, token: str) -> AccessToken:
        client = cls._get_client_from_token(token)
        payload = cls.validate(token, client)
        access_token = AccessToken.from_payload(token, payload, client)
        return access_token
