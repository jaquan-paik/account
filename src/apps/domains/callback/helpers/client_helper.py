from oauth2_provider.models import AbstractApplication

from apps.domains.oauth2.models import Application


class ClientHelper:
    @classmethod
    def get_client(cls, client_id: str):
        client = Application.objects.get(client_id=client_id)

        #  Authorization code 방식만 구현됨
        if client.authorization_grant_type != AbstractApplication.GRANT_AUTHORIZATION_CODE:
            raise NotImplementedError()

        return client
