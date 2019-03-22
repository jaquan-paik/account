from apps.domains.oauth2.models import Application as Client


class ClientRepository:
    @staticmethod
    def get_by_client_id(client_id: str) -> Client:
        return Client.objects.get(client_id=client_id)
