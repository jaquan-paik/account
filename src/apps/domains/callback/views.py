from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.domains.callback.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY
from apps.domains.callback.dtos import OAuth2Data
from apps.domains.callback.helpers.oauth2_data_helper import OAuth2PersistentHelper
from apps.domains.callback.helpers.token_helper import TokenCodeHelper
from apps.domains.callback.helpers.url_helper import UrlHelper
from apps.domains.callback.services.cookie_service import CookieService
from apps.domains.callback.services.token_refresh_service import TokenRefreshService
from apps.domains.oauth2.exceptions import JwtTokenErrorException
from apps.domains.oauth2.token import JwtHandler
from lib.django.http.response import HttpResponseUnauthorized
from lib.utils.url import generate_query_url


class AuthorizeView(View):
    def get(self, request):
        state = request.GET.get('state', None)
        client_id = request.GET.get('client_id', None)
        redirect_uri = request.GET.get('redirect_uri', None)

        oauth2_data = OAuth2Data(state, client_id, redirect_uri)
        oauth2_data.validate_client()
        oauth2_data.validate_redirect_uri()

        OAuth2PersistentHelper.set(request.session, oauth2_data)

        params = {
            'client_id': oauth2_data.client_id,
            'redirect_uri': UrlHelper.get_redirect_uri(),
            'response_type': 'code',
        }
        if state:
            params['state'] = state

        url = generate_query_url(reverse('oauth2_provider:authorize'), params)
        return HttpResponseRedirect(url)


class CallbackView(View):
    def get(self, request):
        code = request.GET.get('code', None)
        state = request.GET.get('state', None)

        oauth2_data = OAuth2PersistentHelper.get(request.session)
        oauth2_data.code = code
        oauth2_data.validate_state(state)
        oauth2_data.validate_client()
        oauth2_data.validate_redirect_uri()

        access_token, refresh_token = TokenCodeHelper.get_tokens(oauth2_data.client, oauth2_data.code, oauth2_data.state)

        redirect_uri = generate_query_url(oauth2_data.redirect_uri, {
            'state': state,
        })

        response = HttpResponseRedirect(redirect_uri)
        CookieService.add_token_cookie(request, response, access_token, refresh_token)

        return response


@method_decorator(csrf_exempt, name='dispatch')
class TokenView(View):
    def post(self, request):
        cookie_access_token = request.COOKIES.get(ACCESS_TOKEN_COOKIE_KEY, None)
        cookie_refresh_token = request.COOKIES.get(REFRESH_TOKEN_COOKIE_KEY, None)

        try:
            access_token = JwtHandler.get_access_token(cookie_access_token)
        except JwtTokenErrorException:
            try:
                new_access_token, new_refresh_token = TokenRefreshService.refresh(cookie_refresh_token)

            except PermissionDenied:
                response = HttpResponseUnauthorized()
                CookieService.clear_token_cookie(request, response)
                return response

            else:
                data = {
                    'expires_at': new_access_token.expires_at,
                    'expires_in': new_access_token.expires_in,
                }
                response = JsonResponse(data)
                CookieService.add_token_cookie(request, response, new_access_token, new_refresh_token)
                return response

        else:
            data = {
                'expires_at': access_token.expires,
                'expires_in': int(access_token.expires - datetime.now().timestamp()),
            }
            return JsonResponse(data)
