from django.core.exceptions import ObjectDoesNotExist

from apps.domains.oauth2.exceptions import NotExistedClient, NotInHouseClient, InvalidRedirectUri
from apps.domains.oauth2.models import Application as Client
from apps.domains.oauth2.repositories.client_repository import ClientRepository
from lib.utils.url import is_same_url_until_domain, is_same_url


class ClientService:
    @classmethod
    def get_client(cls, client_id: str) -> Client:
        try:
            client = ClientRepository.get_by_client_id(client_id)
        except ObjectDoesNotExist:
            raise NotExistedClient

        return client

    @classmethod
    def get_in_house_client(cls, client_id: str) -> Client:
        client = cls.get_client(client_id)

        if not client.is_in_house:
            raise NotInHouseClient

        return client

    @staticmethod
    def assert_in_house_client_redirect_uri(client: Client, redirect_uri: str):
        if not client.is_in_house:
            raise NotInHouseClient

        for client_redirect_uri in client.redirect_uris.split():
            if is_same_url_until_domain(redirect_uri, client_redirect_uri):
                return

        raise InvalidRedirectUri

    @classmethod
    def assert_client_redirect_uri(cls, client: Client, redirect_uri: str):
        if client.is_in_house:
            cls.assert_in_house_client_redirect_uri(client, redirect_uri)
            return

        for client_redirect_uri in client.redirect_uris.split():
            if is_same_url(redirect_uri, client_redirect_uri):
                return

        raise InvalidRedirectUri
