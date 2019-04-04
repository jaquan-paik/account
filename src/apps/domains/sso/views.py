from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView
from ridi_django_oauth2.decorators import login_required

from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper
from apps.domains.ridi.services.in_house_client_credentials_service import InHouseClientCredentialsService
from apps.domains.ridi.views import is_auto_login_request
from apps.domains.sso.config import SSOConfig
from apps.domains.sso.exceptions import FailVerifyOtpException
from apps.domains.sso.forms import SSOLoginForm
from apps.domains.sso.serializers import SSOOtpGenerateResponseSerializer, \
    SSOOtpVerifyResponseSerializer, SSOOtpVerifyRequestSerializer
from apps.domains.sso.services.sso_otp_service import SSOOtpService
from infra.configure.config import GeneralConfig
from infra.network.constants.api_status_code import ApiStatusCodes
from lib.decorators.ridi_oauth2_access_token_login import ridi_oauth2_access_token_login
from lib.django.views.api.mixins import ResponseMixin
from lib.log.logger import logger
from lib.ridibooks.internal_server_auth.decorators import ridi_internal_auth
from lib.utils.url import generate_query_url

_SSO_AUDIENCE = 'sso'


@method_decorator(ridi_oauth2_access_token_login, 'dispatch')
class GenerateSSOOtpView(ResponseMixin, APIView):
    @login_required()
    def post(self, request):
        otp = SSOOtpService.generate(SSOConfig.get_sso_otp_key(), request.user.idx, request.user.token_info.client_id)
        return self.success_response(
            data=SSOOtpGenerateResponseSerializer({'otp': otp}).data
        )


class VerifySSOOtpView(ResponseMixin, APIView):
    @ridi_internal_auth
    def get(self, request):
        serializer = SSOOtpVerifyRequestSerializer(request.params)
        if not serializer.is_valid():
            code = self.make_response_code(ApiStatusCodes.C_400_BAD_REQUEST)
            return self.fail_response(code, serializer.errors)

        try:
            u_idx, _ = SSOOtpService.verify(SSOConfig.get_sso_otp_key(), serializer.validated_data['otp'])
        except FailVerifyOtpException as e:
            code = self.make_response_code(ApiStatusCodes.C_401_UNAUTHORIZED)
            return self.fail_response(code, {'message': e.msg})

        return self.success_response(
            data=SSOOtpVerifyResponseSerializer({'u_idx': u_idx}).data
        )


class SSOLoginView(View):
    def get(self, request):
        form = SSOLoginForm(request.GET, domain=SSOConfig.get_sso_redirect_domain())
        if not form.is_valid():
            return HttpResponseBadRequest()

        otp = form.cleaned_data['otp']
        redirect_uri = form.cleaned_data.get('redirect_uri', None)
        if redirect_uri:
            return self._login_with_store(otp, redirect_uri)

        try:
            u_idx, client_id = SSOOtpService.verify(SSOConfig.get_sso_otp_key(), otp)
            access_token, refresh_token = InHouseClientCredentialsService.get_tokens(
                client_id=client_id, u_idx=u_idx, audience=_SSO_AUDIENCE
            )
        except Exception:
            return HttpResponseForbidden()

        response = HttpResponseRedirect(GeneralConfig.get_store_url())
        ResponseCookieHelper.add_token_cookie(response, access_token, refresh_token, is_auto_login_request(request))
        return response

    def _login_with_store(self, otp: str, redirect_uri: str):
        try:
            u_idx, _ = SSOOtpService.verify(SSOConfig.get_sso_otp_key(), otp)
        except FailVerifyOtpException:
            return HttpResponseForbidden()

        new_otp = SSOOtpService.generate(SSOConfig.get_sso_otp_key(), u_idx)
        return redirect(
            generate_query_url(SSOConfig.get_sso_store_login_url(), {'token': new_otp, 'return_url': redirect_uri})
        )
