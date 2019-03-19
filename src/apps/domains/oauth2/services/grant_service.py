from apps.domains.oauth2.constants import DEFAULT_SCOPE
from apps.domains.oauth2.models import Application as Client, Grant
from apps.domains.oauth2.repositories.grant_repository import GrantRepository


class GrantService:
    @staticmethod
    def create_grant(client: Client, redirect_uri: str, u_idx: int, scope=DEFAULT_SCOPE) -> Grant:
        grant = GrantRepository.create_grant(client, redirect_uri, u_idx, scope)
        return grant
#
