from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from requests import HTTPError
from rest_framework.views import APIView

from apps.domains.ridi.helpers.client_helper import ClientHelper
from apps.domains.ridi.helpers.token_request_helper import TokenRequestHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper
from apps.domains.ridi.mixins import TokenCookieMixin
from apps.domains.ridi.response import InHouseHttpResponseRedirect
from apps.domains.ridi.schemas import TokenGetSchema
from apps.domains.ridi.services.token_refresh_service import TokenRefreshService
from apps.domains.oauth2.exceptions import JwtTokenErrorException
from apps.domains.oauth2.token import JwtHandler
from apps.domains.ridi.services.ridi_service import RidiService
from apps.domains.ridi.forms import AuthorizeForm, CallbackForm, TokenForm

from infra.network.constants.http_status_code import HttpStatusCodes

from lib.django.http.response import HttpResponseUnauthorized


class AuthorizeView(LoginRequiredMixin, View):
    def get(self, request):
        valid_data = AuthorizeForm(request.GET).get_valid_data_with_client_check()
        url = RidiService.get_oauth2_authorize_url(valid_data['client_id'], valid_data['redirect_uri'], request.user.idx)
        return HttpResponseRedirect(url)


class CallbackView(TokenCookieMixin, View):
    def get(self, request):

        # TODO : ------ 재배포시 삭제 시작 부분 ------
        deprecated = request.GET.get('deprecated', None)
        code = request.GET.get('code', None)
        client_id = request.GET.get('client_id', None)
        in_house_redirect_uri = request.GET.get('in_house_redirect_uri', None)
        if deprecated:
            try:
                access_token, refresh_token = TokenRequestHelper.get_tokens(
                    grant_type='authorization_code', client=ClientHelper.get_in_house_client(client_id),
                    code=code, redirect_uri=f'{UrlHelper.get_redirect_url(in_house_redirect_uri, client_id)}&deprecated=1'
                )
            except HTTPError as e:
                return JsonResponse(data=e.response.json(), status=e.response.status_code)

            root_domain = UrlHelper.get_root_domain(self.request)
            response = InHouseHttpResponseRedirect(in_house_redirect_uri)
            self.add_token_cookie(
                response=response, access_token=access_token, refresh_token=refresh_token, root_domain=root_domain
            )

            return response
        # TODO : ------- 재배포시 삭제 -------

        valid_data = CallbackForm(request.GET).get_valid_data_with_state_check(request.user.idx)
        try:
            access_token, refresh_token = RidiService.get_token(
                valid_data['code'], valid_data['client_id'], valid_data['in_house_redirect_uri']
            )
        except HTTPError as e:
            return JsonResponse(data=e.response.json(), status=e.response.status_code)

        root_domain = UrlHelper.get_root_domain(self.request)
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
        valid_data = TokenForm(request.COOKIES).get_valid_data()
        root_domain = UrlHelper.get_root_domain(self.request)
        access_token = JwtHandler.get_access_token(valid_data['access_token'])

        try:
            if not access_token:
                access_token, refresh_token = TokenRefreshService.refresh(valid_data['refresh_token'])
                data = RidiService.get_token_data_info(access_token)
                response = JsonResponse(data)
                self.add_token_cookie(
                    response=response, access_token=access_token, refresh_token=refresh_token,
                    root_domain=root_domain
                )
            else:
                data = RidiService.get_token_info(access_token)
                response = JsonResponse(data)

            return response
        except HTTPError as e:
            return JsonResponse(data=e.response.json(), status=e.response.status_code)


class LogoutView(TokenCookieMixin, View):
    def get(self, request):
        root_domain = self.get_root_domain()
        return_url = request.GET.get('return_url', f'https://{root_domain}')

        response = HttpResponseRedirect(return_url)
        self.clear_token_cookie(response=response, root_domain=root_domain)
        return response
