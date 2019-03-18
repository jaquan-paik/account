class OAuth2AuthorizationCodeService:
    pass
    # @staticmethod
    # def _authenticate_user(skip_authorization: bool):
    #     if not skip_authorization:  # TODO: 후에 open api시 변경 필요
    #         raise InvalidClientError
    #
    # @classmethod
    # def create_code(cls, client_id: str, redirect_uri: str, u_idx: int) -> str:
    #     client = ClientService.get_client(client_id, GrantType.AUTHORIZATION_CODE)
    #     cls._authenticate_user(client.skip_authorization)
    #     code = GrantService.create_grant(client, redirect_uri, u_idx).code
    #     return code
    #
    # @staticmethod
    # def create_token(client_id: str, client_secret: str, redirect_uri: str, code: str) -> dict:
    #     client = ClientService.get_confidential_client(client_id, client_secret, GrantType.AUTHORIZATION_CODE)
    #     grant = GrantService.get_grant(client, redirect_uri, code)
    #     return TokenHelper.generate_tokens(grant.user, client, [SCOPE])
