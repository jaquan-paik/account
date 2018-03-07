from datetime import datetime

from django.db import transaction
from oauth2_provider.oauth2_validators import Grant, RefreshToken


class RevokeTokenService:
    @classmethod
    def revoke_expired(cls):
        now = datetime.now()
        cls.revoke_by_expires(now)

    @staticmethod
    @transaction.atomic()
    def revoke_by_expires(expires: datetime):
        RefreshToken.objects.filter(expires__lte=expires).delete()
        Grant.objects.filter(expires__lte=expires).delete()
