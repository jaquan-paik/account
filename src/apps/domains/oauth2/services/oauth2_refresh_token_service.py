from apps.domains.oauth2.constants import DEFAULT_SCOPE
from apps.domains.oauth2.exceptions import InvalidRefreshToken
from apps.domains.oauth2.services.client_service import ClientService
from apps.domains.oauth2.services.refresh_token_service import RefreshTokenService
from apps.domains.oauth2.services.token_service import TokenService


class OAuth2RefreshTokenService:
    @staticmethod
    def get_tokens(client_id: str, client_secret: str, refresh_token: str):
        client = ClientService.get_confidential_client(client_id, client_secret)
        refresh_token = RefreshTokenService.get_by_token(refresh_token)
        if refresh_token.application.client_id != client_id:
            raise InvalidRefreshToken
        return TokenService.generate(client, refresh_token.user, [DEFAULT_SCOPE])
