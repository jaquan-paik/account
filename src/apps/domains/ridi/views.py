from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.domains.ridi.helpers.client_helper import ClientHelper
from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper
from apps.domains.ridi.helpers.token_request_helper import TokenRequestHelper
from apps.domains.ridi.helpers.token_helper import TokenHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper
from apps.domains.ridi.response import InHouseHttpResponseRedirect
from apps.domains.ridi.schemas import TokenGetSchema
from apps.domains.ridi.services.token_refresh_service import TokenRefreshService
from apps.domains.ridi.services.authorization_code_service import AuthorizationCodeService
from apps.domains.oauth2.token import JwtHandler
from apps.domains.ridi.forms import AuthorizeForm, CallbackForm, TokenForm

from infra.network.constants.http_status_code import HttpStatusCodes
from lib.decorators.cookie_handler import clear_tokens_in_cookie
from lib.decorators.exception_handler import exception_handler


class AuthorizeView(LoginRequiredMixin, View):
    def get(self, request):
        valid_data = AuthorizeForm(request.GET).get_valid_data_with_client_check()
        url = AuthorizationCodeService.get_oauth2_authorize_url(valid_data['client_id'], valid_data['redirect_uri'], request.user.idx)
        return HttpResponseRedirect(url)


class CallbackView(View):
    @exception_handler
    def get(self, request):
        # TODO : ------ 재배포시 삭제 시작 부분 ------
        deprecated = request.GET.get('deprecated', None)
        code = request.GET.get('code', None)
        client_id = request.GET.get('client_id', None)
        in_house_redirect_uri = request.GET.get('in_house_redirect_uri', None)
        if deprecated:
            access_token, refresh_token, = TokenRequestHelper.get_tokens(
                grant_type='authorization_code', client=ClientHelper.get_in_house_client(client_id),
                code=code, redirect_uri=f'{UrlHelper.get_redirect_url(in_house_redirect_uri, client_id)}&deprecated=1'
            )

            response = InHouseHttpResponseRedirect(in_house_redirect_uri)
            ResponseCookieHelper.add_token_cookie(response, access_token, refresh_token, UrlHelper.get_root_domain(request))
            return response
        # TODO : ------- 재배포시 삭제 -------

        valid_data = CallbackForm(request.GET).get_valid_data_with_state_check(request.user.idx)
        access_token, refresh_token, = AuthorizationCodeService.get_tokens(
            valid_data['code'], valid_data['client_id'], valid_data['in_house_redirect_uri']
        )
        response = InHouseHttpResponseRedirect(valid_data['in_house_redirect_uri'])
        ResponseCookieHelper.add_token_cookie(response, access_token, refresh_token, UrlHelper.get_root_domain(request))
        return response


class CompleteView(View):
    def get(self, request):
        return JsonResponse(data={}, status=HttpStatusCodes.C_200_OK)


class TokenView(APIView):
    @swagger_auto_schema(**TokenGetSchema.to_swagger_schema())
    @exception_handler
    def post(self, request):
        valid_data = TokenForm(request.COOKIES).get_valid_data()
        access_token = JwtHandler.get_access_token(valid_data['access_token'])
        if not access_token:
            access_token, refresh_token = TokenRefreshService.get_tokens(valid_data['refresh_token'])
            data = TokenHelper.get_token_data_info(access_token)
            response = JsonResponse(data)
            ResponseCookieHelper.add_token_cookie(response, access_token, refresh_token, UrlHelper.get_root_domain(request))
        else:
            data = TokenHelper.get_token_info(access_token)
            response = JsonResponse(data)

        return response


class LogoutView(View):
    @clear_tokens_in_cookie
    def get(self, request):
        root_domain = UrlHelper.get_root_domain(self.request)
        return_url = request.GET.get('return_url', f'https://{root_domain}')
        response = HttpResponseRedirect(return_url)
        return response
