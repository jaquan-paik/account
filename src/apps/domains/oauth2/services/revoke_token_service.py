from datetime import datetime
from time import sleep
from typing import List

from django.db import transaction
from oauth2_provider.oauth2_validators import Grant, RefreshToken


class RevokeTokenService:
    @classmethod
    def revoke_expired(cls):
        now = datetime.now()
        cls.revoke_by_expires(now)

    @classmethod
    def revoke_by_expires(cls, expires: datetime, revoke_per_iter: int=1000):
        while True:
            refresh_tokens = RefreshToken.objects.filter(expires__lte=expires)[0:revoke_per_iter]
            if len(refresh_tokens) == 0:
                break

            cls.revoke_refresh_tokens(refresh_tokens)
            sleep(1)

        while True:
            grants = Grant.objects.filter(expires__lte=expires)[0:revoke_per_iter]
            if len(grants) == 0:
                break

            cls.revoke_grants(grants)
            sleep(1)

    @staticmethod
    @transaction.atomic()
    def revoke_refresh_tokens(refresh_tokens: List[RefreshToken]):
        for refresh_token in refresh_tokens:
            refresh_token.revoke()

    @staticmethod
    @transaction.atomic()
    def revoke_grants(grants: List[Grant]):
        for grant in grants:
            grant.revoke()
