from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.domains.callback.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY, ROOT_DOMAIN_SESSION_KEY, CookieRootDomains
from apps.domains.callback.dtos import OAuth2Data
from apps.domains.callback.helpers.oauth2_data_helper import OAuth2PersistentHelper
from apps.domains.callback.helpers.token_helper import TokenCodeHelper
from apps.domains.callback.helpers.url_helper import UrlHelper
from apps.domains.callback.mixins import TokenCookieMixin
from apps.domains.callback.services.token_refresh_service import TokenRefreshService
from apps.domains.oauth2.exceptions import JwtTokenErrorException
from apps.domains.oauth2.token import JwtHandler
from lib.django.http.response import HttpResponseUnauthorized
from lib.utils.url import generate_query_url


class AuthorizeView(TokenCookieMixin, View):
    def get(self, request):
        state = request.GET.get('state', None)
        client_id = request.GET.get('client_id', None)
        redirect_uri = request.GET.get('redirect_uri', None)

        oauth2_data = OAuth2Data(state, client_id, redirect_uri)
        oauth2_data.validate_client()
        oauth2_data.validate_redirect_uri()

        OAuth2PersistentHelper.set(request.session, oauth2_data)
        request.session[ROOT_DOMAIN_SESSION_KEY] = self.get_root_domain(request=request)

        params = {
            'client_id': oauth2_data.client_id,
            'redirect_uri': UrlHelper.get_redirect_uri(),
            'response_type': 'code',
        }
        if state:
            params['state'] = state

        url = generate_query_url(reverse('oauth2_provider:authorize'), params)
        return HttpResponseRedirect(url)


class CallbackView(TokenCookieMixin, View):
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

        root_domain = CookieRootDomains.to_string(request.session[ROOT_DOMAIN_SESSION_KEY])
        response = HttpResponseRedirect(redirect_uri)
        self.add_token_cookie(response=response, access_token=access_token, refresh_token=refresh_token, root_domain=root_domain)

        return response


@method_decorator(csrf_exempt, name='dispatch')
class TokenView(TokenCookieMixin, View):
    def post(self, request):
        cookie_access_token = self.get_cookie(request, ACCESS_TOKEN_COOKIE_KEY)
        cookie_refresh_token = self.get_cookie(request, REFRESH_TOKEN_COOKIE_KEY)
        root_domain = UrlHelper.get_root_domain(request)

        try:
            access_token = JwtHandler.get_access_token(cookie_access_token)
        except JwtTokenErrorException:
            try:
                new_access_token, new_refresh_token = TokenRefreshService.refresh(cookie_refresh_token)

            except PermissionDenied:
                response = HttpResponseUnauthorized()
                self.clear_token_cookie(response=response, root_domain=root_domain)
                return response

            else:
                data = {
                    'expires_at': new_access_token.expires_at,
                    'expires_in': new_access_token.expires_in,
                }
                response = JsonResponse(data)
                self.add_token_cookie(
                    response=response, access_token=new_access_token, refresh_token=new_refresh_token, root_domain=root_domain
                )
                return response

        else:
            data = {
                'expires_at': access_token.expires,
                'expires_in': int(access_token.expires - datetime.now().timestamp()),
            }
            return JsonResponse(data)
