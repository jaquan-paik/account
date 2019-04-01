from django.views import View
from rest_framework.views import APIView
from ridi_django_oauth2.decorators import login_required

from apps.domains.sso.constants import SSO_TOKEN_TTL
from apps.domains.sso.exceptions import FailVerifyTokenException
from apps.domains.sso.serializers import GenerateTokenResponseSerializer, VerifyTokenRequestSerializer, \
    VerifyTokenResponseSerializer
from apps.domains.sso.services.sso_token_service import SSOTokenService
from infra.network.constants.api_status_code import ApiStatusCodes
from lib.decorators.ridi_oauth2_access_token_login import ridi_oauth2_access_token_login
from lib.django.views.api.mixins import ResponseMixin


class GenerateSSOTokenView(ResponseMixin, APIView):
    @ridi_oauth2_access_token_login
    @login_required()
    def get(self, request):
        token = SSOTokenService.generate(request.user.idx, SSO_TOKEN_TTL)
        return self.success_response(data=GenerateTokenResponseSerializer({'token': token}).data)


class VerifySSOTokenView(ResponseMixin, APIView):
    def get(self, request):
        serializer = VerifyTokenRequestSerializer(request.params)
        if not serializer.is_valid():
            code = self.make_response_code(ApiStatusCodes.C_400_BAD_REQUEST)
            return self.fail_response(code)

        try:
            u_idx = SSOTokenService.verify(serializer.validated_data['token'])
        except FailVerifyTokenException as e:
            code = self.make_response_code(ApiStatusCodes.C_400_BAD_REQUEST)
            return self.fail_response(code, {'message': e.msg})

        return self.success_response(data=VerifyTokenResponseSerializer({'u_idx': u_idx}).data)


class SSOLoginView(View):
    def get(self, request):
        pass
