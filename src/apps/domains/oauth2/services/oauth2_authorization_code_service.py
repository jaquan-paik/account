from apps.domains.oauth2.services.client_service import ClientService
from apps.domains.oauth2.services.grant_service import GrantService


class OAuth2AuthorizationCodeService:
    @staticmethod
    def _authenticate_user(skip_authorization: bool):
        if not skip_authorization:
            raise NotImplementedError

    @classmethod
    def create_code(cls, client_id: str, redirect_uri: str, u_idx: int) -> str:
        client = ClientService.get_client(client_id)
        cls._authenticate_user(client.skip_authorization)
        ClientService.assert_house_client_redirect_uri(client, redirect_uri)
        code = GrantService.create_grant(client, redirect_uri, u_idx).code
        return code

    # @staticmethod
    # def create_token(client_id: str, client_secret: str, redirect_uri: str, code: str) -> dict:
    #     client = ClientService.get_confidential_client(client_id, client_secret, GrantType.AUTHORIZATION_CODE)
    #     grant = GrantService.get_grant(client, redirect_uri, code)
    #     return TokenHelper.generate_tokens(grant.user, client, [SCOPE])
#
