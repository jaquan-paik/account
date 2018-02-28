from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from apps.domains.callback.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY
from apps.domains.callback.dtos import OAuth2Data, TokenData
from apps.domains.callback.helpers.oauth2_data_helper import OAuth2PersistentHelper
from apps.domains.callback.helpers.token_helper import TokenHelper
from apps.domains.callback.helpers.url_helper import UrlHelper
from infra.configure.config import GeneralConfig
from lib.utils.url import generate_query_url


class LoginView(View):
    def get(self, request):
        state = request.GET.get('state', None)
        client_id = request.GET.get('client_id', None)
        redirect_uri = request.GET.get('redirect_uri', None)

        oauth2_data = OAuth2Data(state, client_id, redirect_uri)
        oauth2_data.validate_client()

        OAuth2PersistentHelper.set(request.session, oauth2_data)

        url = generate_query_url(reverse('oauth2_provider:authorize'), {
            'state': state,
            'client_id': oauth2_data.client_id,
            'redirect_uri': UrlHelper.get_redirect_uri(),
            'response_type': 'code',
        })

        return HttpResponseRedirect(url)


class CallbackView(View):
    @staticmethod
    def _set_token_cookie(response, key: str, token_data: TokenData):
        response.set_cookie(
            key, token_data.token, max_age=token_data.expires_in, expires=token_data.cookie_expire_time,
            domain=GeneralConfig.get_root_domain(), secure=True, httponly=True
        )

    def get(self, request):
        code = request.GET.get('code', None)
        state = request.GET.get('state', None)

        oauth2_data = OAuth2PersistentHelper.get(request.session)
        oauth2_data.code = code
        oauth2_data.validate_state(state)
        oauth2_data.validate_client()

        access_token, refresh_token = TokenHelper.get_tokens(oauth2_data)

        response = HttpResponseRedirect(oauth2_data.redirect_uri)
        self._set_token_cookie(response, ACCESS_TOKEN_COOKIE_KEY, access_token)
        self._set_token_cookie(response, REFRESH_TOKEN_COOKIE_KEY, refresh_token)

        return response
