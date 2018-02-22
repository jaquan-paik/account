from datetime import datetime

import jwt
from django.conf import settings
from oauth2_provider.settings import oauth2_settings
from oauthlib.oauth2 import Server
from oauthlib.oauth2.rfc6749.tokens import random_token_generator


def jwt_token_generator(request, refresh_token=False):
    secret = settings.OAUTH2_ACCESS_JWT_SECRET
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

    return jwt.encode(payload, secret, algorithm='HS256').decode()


class RidiServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(token_generator=jwt_token_generator, refresh_token_generator=random_token_generator, *args, **kwargs)
