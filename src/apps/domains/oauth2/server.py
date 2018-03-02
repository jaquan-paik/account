from datetime import datetime


from oauth2_provider.settings import oauth2_settings
from oauthlib.oauth2 import Server
from oauthlib.oauth2.rfc6749.tokens import random_token_generator

from apps.domains.oauth2.constants import JwtAlg


def jwt_token_generator(request, refresh_token=False):
    import jwt
    user = request.user
    client = request.client
    scopes = request.scopes

    payload = {
        'sub': user.id,
        'u_idx': user.idx,
        'exp': round(datetime.now().timestamp()) + oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        'client_id': client.client_id,
        'scope': scopes
    }

    if client.jwt_alg == JwtAlg.HS256:
        return jwt.encode(payload, client.jwt_hs_256_secret, algorithm=JwtAlg.HS256).decode()

    raise NotImplementedError(f'Jwt alg is not implemented: {client.jwt_alg}')


class RidiServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(token_generator=jwt_token_generator, refresh_token_generator=random_token_generator, *args, **kwargs)
