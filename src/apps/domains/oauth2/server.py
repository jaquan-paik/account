from oauthlib.oauth2 import Server
from oauthlib.oauth2.rfc6749.tokens import random_token_generator

from apps.domains.oauth2.token import JwtHandler


# pylint:disable=too-many-ancestors
class RidiServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(token_generator=JwtHandler.generate, refresh_token_generator=random_token_generator, *args, **kwargs)
