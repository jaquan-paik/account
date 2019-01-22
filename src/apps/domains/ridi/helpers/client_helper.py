from oauth2_provider.models import AbstractApplication
from urllib.parse import urlparse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from apps.domains.oauth2.models import Application


class ClientHelper:
    @classmethod
    def get_client(cls, client_id: str) -> Application:
        try:
            client = Application.objects.get(client_id=client_id)
        except ObjectDoesNotExist:
            raise PermissionDenied()

        if client.authorization_grant_type != AbstractApplication.GRANT_AUTHORIZATION_CODE:
            raise NotImplementedError()

        return client

    @classmethod
    def get_in_house_client(cls, client_id: str) -> Application:
        client = cls.get_client(client_id)

        if not client.is_in_house:
            raise PermissionDenied()

        return client

    @staticmethod
    def validate_redirect_uri(client: Application, redirect_uri: str):
        parsed_uri = urlparse(redirect_uri)
        for allowed_uri in client.redirect_uris.split():
            parsed_allowed_uri = urlparse(allowed_uri)

            if parsed_allowed_uri.scheme == parsed_uri.scheme and parsed_allowed_uri.netloc == parsed_uri.netloc:
                return True
        raise PermissionDenied()
