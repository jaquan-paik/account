from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.domains.oauth2.exceptions import JwtTokenErrorException
from apps.domains.oauth2.token import JwtHandler
from apps.domains.ridi.forms import AuthorizeForm, CallbackForm, TokenForm
from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper
from apps.domains.ridi.helpers.state_helper import StateHelper
from apps.domains.ridi.helpers.token_helper import TokenHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper
from apps.domains.ridi.schemas import TokenGetSchema
from apps.domains.ridi.services.authorization_code_service import AuthorizationCodeService
from apps.domains.ridi.services.token_refresh_service import TokenRefreshService
from infra.configure.config import GeneralConfig
from infra.network.constants.http_status_code import HttpStatusCodes
from lib.base.response import InHouseHttpResponseRedirect, get_invalid_form_template_response
from lib.decorators.session_login import ridibooks_session_login_required
from lib.django.http.response import HttpResponseUnauthorized
from lib.ridibooks.common.constants import AUTO_LOGIN_COOKIE_KEY, AUTO_LOGIN_ON_COOKIE_VALUE


def is_auto_login_request(request) -> bool:
    return request.COOKIES.get(AUTO_LOGIN_COOKIE_KEY, '0') == AUTO_LOGIN_ON_COOKIE_VALUE


class AuthorizeView(View):
    @ridibooks_session_login_required()
    def get(self, request):
        authorize_form = AuthorizeForm(request.GET)
        if not authorize_form.is_valid():
            return get_invalid_form_template_response(request, authorize_form)
        cleaned_data = authorize_form.clean()
        url = AuthorizationCodeService.get_oauth2_authorize_url(cleaned_data['client_id'], cleaned_data['redirect_uri'], request.user.idx)
        return HttpResponseRedirect(url)


class CallbackView(View):
    @ridibooks_session_login_required()
    def get(self, request):
        if request.GET.get('deprecated', None) or len(request.GET.get('state', '')) == 10:  # 현재 지원되지 않는 state의 길이가 10이다.
            return HttpResponseRedirect(GeneralConfig.get_store_url())

        callback_form = CallbackForm(request.GET)
        if not callback_form.is_valid():
            return get_invalid_form_template_response(request, callback_form)
        cleaned_data = callback_form.clean()

        StateHelper.validate_state(cleaned_data.get('state'), request.user.idx)

        access_token, refresh_token = AuthorizationCodeService.get_tokens(
            cleaned_data['code'], cleaned_data['client_id'], cleaned_data['in_house_redirect_uri']
        )
        response = InHouseHttpResponseRedirect(cleaned_data['in_house_redirect_uri'])
        ResponseCookieHelper.add_token_cookie(response, access_token, refresh_token, is_auto_login_request(request))
        return response


class CompleteView(View):
    def get(self, request):
        return JsonResponse(data={}, status=HttpStatusCodes.C_200_OK)


class TokenView(APIView):
    @swagger_auto_schema(**TokenGetSchema.to_swagger_schema())
    def post(self, request):
        token_form = TokenForm(TokenHelper.get_token_data_from_cookie(request.COOKIES))
        if not token_form.is_valid():
            return JsonResponse(data=token_form.errors, status=HttpStatusCodes.C_400_BAD_REQUEST)
        cleaned_data = token_form.clean()

        try:
            access_token = JwtHandler.get_access_token(cleaned_data['access_token'])
            data = TokenHelper.get_token_info(access_token)
            response = JsonResponse(data)

        except JwtTokenErrorException:  # access_token 이 valid 하지 않으면 refresh_token 으로 새로 토큰들을 요청한다.
            try:
                access_token_data, refresh_token_data = TokenRefreshService.get_tokens(cleaned_data['refresh_token'])
                response = JsonResponse(TokenHelper.get_token_data_info(access_token_data))
                ResponseCookieHelper.add_token_cookie(response, access_token_data, refresh_token_data, is_auto_login_request(request))
            except PermissionDenied:
                response = HttpResponseUnauthorized()
                ResponseCookieHelper.clear_token_cookie(response)

        return response


class LogoutView(View):
    def get(self, request):
        return_url = request.GET.get('return_url', None)
        if not return_url:
            return_url = f'https://{UrlHelper.get_root_uri()}'

        response = HttpResponseRedirect(return_url)
        ResponseCookieHelper.clear_token_cookie(response)
        return response
