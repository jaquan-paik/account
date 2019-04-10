from apps.domains.oauth2.constants import DEFAULT_SCOPE
from apps.domains.oauth2.exceptions import InvalidUserError
from apps.domains.oauth2.repositories.user_repository import UserRepository
from apps.domains.oauth2.services.client_service import ClientService
from apps.domains.oauth2.services.token_service import TokenService
from lib.ridibooks.api.exceptions import RidibooksException
from lib.ridibooks.api.store import StoreApi


class OAuth2PasswordTokenService:
    @classmethod
    def get_tokens(cls, client_id: str, client_secret: str, username: str, password: str):
        client = ClientService.get_confidential_client(client_id, client_secret)
        account_info = cls._get_account_info(username, password)
        user = UserRepository.get_or_create(u_idx=account_info['u_idx'], u_id=username)
        return TokenService.generate(client, user, [DEFAULT_SCOPE])

    @staticmethod
    def _get_account_info(username: str, password: str) -> dict:
        try:
            return StoreApi().is_loginable(username, password)
        except RidibooksException:
            raise InvalidUserError
