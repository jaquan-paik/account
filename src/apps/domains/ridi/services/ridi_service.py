from django.urls import reverse

from apps.domains.ridi.helpers.client_helper import ClientHelper
from apps.domains.ridi.helpers.state_helper import StateHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper
from lib.utils.url import generate_query_url


class RidiService:
    @staticmethod
    def get_oauth2_authorize_url(client_id, redirect_uri, u_idx):
        client = ClientHelper.get_in_house_client(client_id)
        ClientHelper.validate_redirect_uri(client, redirect_uri)

        params = {
            'client_id': client.client_id,
            'redirect_uri': UrlHelper.get_redirect_url(redirect_uri, client_id),
            'response_type': 'code',
            'state': StateHelper.create_encrypted_state(u_idx),
        }
        url = generate_query_url(reverse('oauth2_provider:authorize'), params)
        return url
