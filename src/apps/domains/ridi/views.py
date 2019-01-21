from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.domains.oauth2.exceptions import JwtTokenErrorException
from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper
from apps.domains.ridi.helpers.state_helper import StateHelper
from apps.domains.ridi.helpers.token_helper import TokenHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper
from apps.domains.ridi.response import InHouseHttpResponseRedirect, get_invalid_form_template_response
from apps.domains.ridi.schemas import TokenGetSchema
from apps.domains.ridi.services.token_refresh_service import TokenRefreshService
from apps.domains.ridi.services.authorization_code_service import AuthorizationCodeService
from apps.domains.oauth2.token import JwtHandler
from apps.domains.ridi.forms import AuthorizeForm, CallbackForm, TokenForm

from infra.network.constants.http_status_code import HttpStatusCodes
from lib.decorators.cookie_handler import clear_tokens_in_cookie
from lib.decorators.exception_handler import http_error_exception_handler, permission_denied_exception_handler
from lib.log.sentry import message


class AuthorizeView(LoginRequiredMixin, View):
    def get(self, request):
        authorize_form = AuthorizeForm(request.GET)
        if not authorize_form.is_valid():
            return get_invalid_form_template_response(request, authorize_form)
        cleaned_data = authorize_form.clean()
        url = AuthorizationCodeService.get_oauth2_authorize_url(cleaned_data['client_id'], cleaned_data['redirect_uri'], request.user.idx)
        return HttpResponseRedirect(url)


class CallbackView(View):
    @http_error_exception_handler(template_response=True)
    def get(self, request):
        if request.user.is_anonymous:  # TODO: phpsession 이 없어지는 요청에 대해 기록한다. 후에 추이를 보며 방향을 결정
            message('callback:AnonymousUser', extra=request.GET)
            raise PermissionDenied()

        callback_form = CallbackForm(request.GET)
        if not callback_form.is_valid():
            return get_invalid_form_template_response(request, callback_form)
        cleaned_data = callback_form.clean()

        StateHelper.validate_state(cleaned_data.get('state'), request.user.idx)

        access_token, refresh_token = AuthorizationCodeService.get_tokens(
            cleaned_data['code'], cleaned_data['client_id'], cleaned_data['in_house_redirect_uri']
        )
        root_domain = UrlHelper.get_root_domain(self.request)
        response = InHouseHttpResponseRedirect(cleaned_data['in_house_redirect_uri'])
        ResponseCookieHelper.add_token_cookie(response, access_token, refresh_token, root_domain)
        return response


class CompleteView(View):
    def get(self, request):
        return JsonResponse(data={}, status=HttpStatusCodes.C_200_OK)


class TokenView(APIView):
    @swagger_auto_schema(**TokenGetSchema.to_swagger_schema())
    @permission_denied_exception_handler
    @http_error_exception_handler()
    def post(self, request):
        token_form = TokenForm(TokenHelper.get_token_data_from_cookie(request.COOKIES))
        if not token_form.is_valid():
            return JsonResponse(data=token_form.errors, status=HttpStatusCodes.C_400_BAD_REQUEST)
        cleaned_data = token_form.clean()
        root_domain = UrlHelper.get_root_domain(self.request)

        try:
            access_token = JwtHandler.get_access_token(cleaned_data['access_token'])

        except JwtTokenErrorException:
            access_token, refresh_token = TokenRefreshService.get_tokens(cleaned_data['refresh_token'])
            data = TokenHelper.get_token_data_info(access_token)
            response = JsonResponse(data)
            ResponseCookieHelper.add_token_cookie(response, access_token, refresh_token, root_domain)

        else:
            data = TokenHelper.get_token_info(access_token)
            response = JsonResponse(data)

        return response


class LogoutView(View):
    @clear_tokens_in_cookie
    def get(self, request):
        root_domain = UrlHelper.get_root_domain(self.request)
        return_url = request.GET.get('return_url', None)
        if not return_url:
            return_url = f'https://{root_domain}'

        response = HttpResponseRedirect(return_url)
        return response
