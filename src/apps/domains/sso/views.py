from django.views import View
from rest_framework.views import APIView
from ridi_django_oauth2.decorators import login_required

from apps.domains.sso.config import SSOConfig
from apps.domains.sso.constants import SSO_TOKEN_TTL, SSOKeyHint
from apps.domains.sso.exceptions import FailVerifyTokenException, NotFoundSSOKeyException
from apps.domains.sso.forms import SSOLoginForm
from apps.domains.sso.serializers import GenerateTokenResponseSerializer, VerifyTokenRequestSerializer, \
    VerifyTokenResponseSerializer, GenerateTokenRequestSerializer
from apps.domains.sso.services.sso_key_service import SSOKeyService
from apps.domains.sso.services.sso_token_service import SSOTokenService
from infra.network.constants.api_status_code import ApiStatusCodes
from lib.decorators.ridi_oauth2_access_token_login import ridi_oauth2_access_token_login
from lib.django.views.api.mixins import ResponseMixin


class GenerateSSOTokenView(ResponseMixin, APIView):
    @ridi_oauth2_access_token_login
    @login_required()
    def get(self, request):
        serializer = GenerateTokenRequestSerializer(request.params)
        if not serializer.is_valid():
            code = self.make_response_code(ApiStatusCodes.C_400_BAD_REQUEST)
            return self.fail_response(code, serializer.errors)

        try:
            key = SSOKeyService.get_key(serializer.validated_data['hint'])
        except NotFoundSSOKeyException as e:
            code = self.make_response_code(ApiStatusCodes.C_400_BAD_REQUEST)
            return self.fail_response(code, {'message': e.msg})

        token = SSOTokenService.generate(request.user.idx, SSO_TOKEN_TTL, key)
        return self.success_response(data=GenerateTokenResponseSerializer({'token': token}).data)


class VerifySSOTokenView(ResponseMixin, APIView):
    def get(self, request):
        serializer = VerifyTokenRequestSerializer(request.params)
        if not serializer.is_valid():
            code = self.make_response_code(ApiStatusCodes.C_400_BAD_REQUEST)
            return self.fail_response(code, serializer.errors)

        try:
            key = SSOKeyService.get_key(serializer.validated_data['hint'])
            u_idx = SSOTokenService.verify(serializer.validated_data['token'], key)
        except (FailVerifyTokenException, NotFoundSSOKeyException) as e:
            code = self.make_response_code(ApiStatusCodes.C_400_BAD_REQUEST)
            return self.fail_response(code, {'message': e.msg})

        return self.success_response(data=VerifyTokenResponseSerializer({'u_idx': u_idx}).data)


class SSOLoginView(View):
    def get(self, request):
        form = SSOLoginForm(request.GET, domain=SSOConfig.get_sso_root_domain())
        if not form.is_valid():
            # redirect to store ? 어디로 ?
            return

        try:
            u_idx = SSOTokenService.verify(form.cleaned_data['token'], SSOKeyService.get_key(SSOKeyHint.VIEWER))
        except FailVerifyTokenException as e:
            return

        token = SSOTokenService.generate(u_idx, SSO_TOKEN_TTL, SSOKeyService.get_key(SSOKeyHint.SESSION_LOGIN))
        return
