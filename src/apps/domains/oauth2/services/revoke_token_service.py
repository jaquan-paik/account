from datetime import datetime

from oauth2_provider.oauth2_validators import Grant, RefreshToken

DEFAULT_REVOKE_COUNT = 1000


class RevokeTokenService:
    @classmethod
    def revoke_expired(cls):
        now = datetime.now()
        cls.revoke_by_expires(now)

    @classmethod
    def revoke_by_expires(cls, expires: datetime, revoke_count: int=DEFAULT_REVOKE_COUNT):
        RefreshToken.objects.revoke_by_expire_date(expires, revoke_count)
        Grant.objects.revoke_by_expire_date(expires, revoke_count)
