from apps.domains.oauth2.constants import DEFAULT_SCOPE, GrantType
from apps.domains.oauth2.exceptions import NotExistedClient
from apps.domains.oauth2.repositories.grant_repository import GrantRepository
from apps.domains.oauth2.services.client_service import ClientService


class OAuth2AuthorizationCodeService:
    @staticmethod
    def _authenticate_user(skip_authorization: bool):
        if not skip_authorization:
            raise NotImplementedError

    @classmethod
    def create_code(cls, client_id: str, redirect_uri: str, u_idx: int) -> str:
        client = ClientService.get_client(client_id)
        authorization_grant_type = client.authorization_grant_type
        if authorization_grant_type != GrantType.OLD_AUTHORIZATION_CODE and authorization_grant_type != GrantType.AUTHORIZATION_CODE:
            raise NotExistedClient
        cls._authenticate_user(client.skip_authorization)
        ClientService.assert_client_redirect_uri(client, redirect_uri)
        code = GrantRepository.create_grant(client, redirect_uri, u_idx, DEFAULT_SCOPE).code
        return code
