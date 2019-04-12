from django.core.exceptions import PermissionDenied
from oauthlib.oauth2 import OAuth2Error

from apps.domains.oauth2.models import Application
from apps.domains.oauth2.services.client_service import ClientService
from lib.utils.url import is_same_url_until_domain


class ClientHelper:
    @classmethod
    def get_in_house_client(cls, client_id: str) -> Application:
        try:
            client = ClientService.get_in_house_client(client_id)
        except OAuth2Error:
            raise PermissionDenied()

        return client

    @staticmethod
    def assert_in_house_client_redirect_uri(client: Application, redirect_uri: str):
        if not client.is_in_house:
            raise PermissionDenied()

        for client_redirect_uri in client.redirect_uris.split():
            if is_same_url_until_domain(redirect_uri, client_redirect_uri):
                return

        raise PermissionDenied()
