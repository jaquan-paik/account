from datetime import timedelta
from django.utils import timezone
from lib.utils.string import generate_random_str

from apps.domains.oauth2.constants import ACCESS_TOKEN_EXPIRE_SECONDS, CODE_LENGTH
from apps.domains.oauth2.models import Grant, Application as Client


class GrantRepository:
    @staticmethod
    def _get_grant_expires():
        return timezone.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)

    @staticmethod
    def _create_random_code():
        return generate_random_str(CODE_LENGTH)

    @classmethod
    def create_grant(cls, client: Client, redirect_uri: str, u_idx: int, scope: str) -> Grant:
        grant = Grant(

            code=cls._create_random_code(), user_id=u_idx, application=client,
            redirect_uri=redirect_uri, scope=scope, expires=cls._get_grant_expires(),
        )
        grant.save()
        return grant
