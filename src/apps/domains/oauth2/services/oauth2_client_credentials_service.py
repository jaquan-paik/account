from typing import Dict

from apps.domains.account.models import User
from apps.domains.oauth2.constants import GrantType, DEFAULT_SCOPE
from apps.domains.oauth2.exceptions import UnsupportedGrantType
from apps.domains.oauth2.services.client_service import ClientService
from apps.domains.oauth2.services.token_service import TokenService


class OAuth2ClientCredentialsService:
    @staticmethod
    def get_tokens(client_id: str, client_secret: str, user: User, aud: str = None) -> Dict:
        client = ClientService.get_confidential_client(client_id, client_secret)
        if not client.allows_grant_type(GrantType.CLIENT_CREDENTIALS):
            raise UnsupportedGrantType()

        return TokenService.generate(client, user, [DEFAULT_SCOPE], aud)
