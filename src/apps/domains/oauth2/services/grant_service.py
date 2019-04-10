from django.core.exceptions import ObjectDoesNotExist

from apps.domains.oauth2.exceptions import InvalidCode, InvalidClient, InvalidRedirectUri
from apps.domains.oauth2.models import Application as Client, Grant
from apps.domains.oauth2.repositories.grant_repository import GrantRepository
from lib.utils.url import is_same_url


class GrantService:
    @staticmethod
    def create_grant(client: Client, redirect_uri: str, u_idx: int, scope: str) -> Grant:
        return GrantRepository.create_grant(client, redirect_uri, u_idx, scope)

    @staticmethod
    def get_grant(client: Client, code: str, redirect_uri: str) -> Grant:
        try:
            grant = GrantRepository.get_grant_by_code(code)
        except ObjectDoesNotExist:
            raise InvalidCode

        if grant.application != client:
            raise InvalidClient

        if not is_same_url(grant.redirect_uri, redirect_uri):
            raise InvalidRedirectUri
        return grant
