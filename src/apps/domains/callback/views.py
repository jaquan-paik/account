from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from requests import HTTPError
from rest_framework.views import APIView

from apps.domains.callback.constants import CookieRootDomains, ROOT_DOMAIN_SESSION_KEY
from apps.domains.callback.helpers.token_helper import TokenCodeHelper
from apps.domains.callback.helpers.url_helper import UrlHelper
from apps.domains.callback.mixins import OAuth2SessionMixin, TokenCookieMixin
from apps.domains.callback.response import InHouseHttpResponseRedirect
from apps.domains.callback.schemas import TokenGetSchema
from apps.domains.callback.services.token_refresh_service import TokenRefreshService
from apps.domains.oauth2.exceptions import JwtTokenErrorException
from apps.domains.oauth2.token import JwtHandler
from infra.network.constants.http_status_code import HttpStatusCodes
from lib.django.http.response import HttpResponseUnauthorized
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY
from lib.utils.string import generate_random_str
from lib.utils.url import generate_query_url


class AuthorizeView(LoginRequiredMixin, OAuth2SessionMixin, TokenCookieMixin, View):  # pylint: disable=too-many-ancestors
    def get(self, request):
        client_id = request.GET.get('client_id', None)
        redirect_uri = request.GET.get('redirect_uri', None)
        state = generate_random_str(10)

        self.set_oauth2_data(client_id, redirect_uri, state)
        self.set_session(key=ROOT_DOMAIN_SESSION_KEY, value=CookieRootDomains.to_value(self.get_root_domain()))

        params = {
            'client_id': client_id,
            'redirect_uri': UrlHelper.get_redirect_url(redirect_uri, client_id),
            'response_type': 'code',
            'state': state,
        }

        url = generate_query_url(reverse('oauth2_provider:authorize'), params)
        return HttpResponseRedirect(url)


class CallbackView(OAuth2SessionMixin, TokenCookieMixin, View):
    def get(self, request):
        code = request.GET.get('code', None)
        state = request.GET.get('state', None)
        oauth2_data = self.get_oauth2_data(code=code, state=state)
        in_house_redirect_uri = request.GET.get('in_house_redirect_uri', oauth2_data.redirect_uri)
        try:
            access_token, refresh_token = TokenCodeHelper.get_tokens(
                oauth2_data.client, oauth2_data.code, UrlHelper.get_redirect_url(in_house_redirect_uri, oauth2_data.client.client_id)
            )
        except HTTPError as e:
            return JsonResponse(data=e.response.json(), status=e.response.status_code)

        root_domain = CookieRootDomains.to_string(self.get_session(key=ROOT_DOMAIN_SESSION_KEY))
        response = InHouseHttpResponseRedirect(in_house_redirect_uri)
        self.add_token_cookie(
            response=response, access_token=access_token, refresh_token=refresh_token, root_domain=root_domain
        )

        return response


class CompleteView(View):
    def get(self, request):
        return JsonResponse(data={}, status=HttpStatusCodes.C_200_OK)


class TokenView(TokenCookieMixin, APIView):
    @swagger_auto_schema(**TokenGetSchema.to_swagger_schema())
    def post(self, request):
        root_domain = self.get_root_domain()
        cookie_access_token = self.get_cookie(request, ACCESS_TOKEN_COOKIE_KEY)
        cookie_refresh_token = self.get_cookie(request, REFRESH_TOKEN_COOKIE_KEY)

        try:
            access_token = JwtHandler.get_access_token(cookie_access_token)
        except JwtTokenErrorException:
            try:
                new_access_token, new_refresh_token = TokenRefreshService.refresh(cookie_refresh_token)

            except PermissionDenied:
                response = HttpResponseUnauthorized()
                self.clear_token_cookie(response=response, root_domain=root_domain)
                return response
            except HTTPError as e:
                return JsonResponse(data=e.response.json(), status=e.response.status_code)

            else:
                data = {
                    'expires_at': new_access_token.expires_at,
                    'expires_in': new_access_token.expires_in,
                }
                response = JsonResponse(data)
                self.add_token_cookie(
                    response=response, access_token=new_access_token, refresh_token=new_refresh_token,
                    root_domain=root_domain
                )
                return response

        else:
            data = {
                'expires_at': access_token.expires,
                'expires_in': int(access_token.expires - datetime.now().timestamp()),
            }
            return JsonResponse(data)


class LogoutView(TokenCookieMixin, View):
    def get(self, request):
        root_domain = self.get_root_domain()
        return_url = request.GET.get('return_url', f'https://{root_domain}')

        response = HttpResponseRedirect(return_url)
        self.clear_token_cookie(response=response, root_domain=root_domain)
        return response
