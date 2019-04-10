from apps.domains.oauth2.constants import DEFAULT_SCOPE, GrantType
from apps.domains.oauth2.exceptions import DisallowedGrantType
from apps.domains.oauth2.repositories.grant_repository import GrantRepository
from apps.domains.oauth2.services.client_service import ClientService
from apps.domains.oauth2.services.grant_service import GrantService
from apps.domains.oauth2.services.token_service import TokenService


class OAuth2AuthorizationCodeService:
    @staticmethod
    def _assert_if_user_grant_client_access_request(skip_authorization: bool):
        if not skip_authorization:  # TODO: open api 지원할 때 로직 추가가 필요하다.
            raise NotImplementedError

    @classmethod
    def create_code(cls, client_id: str, redirect_uri: str, u_idx: int) -> str:
        client = ClientService.get_client(client_id)
        if not client.allows_grant_type(GrantType.OLD_AUTHORIZATION_CODE, GrantType.AUTHORIZATION_CODE):
            raise DisallowedGrantType()

        cls._assert_if_user_grant_client_access_request(client.skip_authorization)
        ClientService.assert_client_redirect_uri(client, redirect_uri)
        code = GrantRepository.create_grant(client, redirect_uri, u_idx, DEFAULT_SCOPE).code
        return code

    @staticmethod
    def get_tokens(client_id: str, client_secret: str, code: str, redirect_uri: str):
        client = ClientService.get_confidential_client(client_id, client_secret)
        grant = GrantService.get_grant(client, code, redirect_uri)
        return TokenService.generate(client, grant.user, [DEFAULT_SCOPE])
