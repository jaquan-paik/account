from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from rest_framework.views import APIView

from apps.domains.account.services.account_info_service import AccountInfoService
from infra.configure.config import GeneralConfig
from infra.network.constants.api_status_code import ApiStatusCodes
from lib.base.exceptions import ErrorException
from lib.django.views.api.mixins import ResponseMixin
from lib.django.views.cookie.mixins import CookieMixin
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY
from lib.ridibooks.common.exceptions import HTTPException, InvalidResponseException, ServerException
from lib.utils.url import generate_query_url
from apps.domains.account.schemas import RidiAccountInfoGetSchema
from drf_yasg.utils import swagger_auto_schema

class RidiLoginView(LoginView):  # pylint: disable=too-many-ancestors
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # 로그인 되어 있으면 Next로 이동한다.
            redirect_to = self.get_success_url()
            if redirect_to == request.path:
                raise ErrorException('LOGIN REDIRECT URL IS SAME!')
        else:
            # 로그인 안되어 있으면 리디북스 홈페이지로 이동하고 돌아온다.
            params = {
                'return_url': request.build_absolute_uri()
            }

            url = GeneralConfig.get_ridibooks_login_url()

            redirect_to = generate_query_url(url, params)

        return HttpResponseRedirect(redirect_to)

    def post(self, request, *args, **kwargs):
        # 로그인 기능이 없기 때문에 막아둔다.
        pass

    def put(self, *args, **kwargs):
        # 로그인 기능이 없기 때문에 막아둔다.
        pass


class RidiAccountInfoView(CookieMixin, ResponseMixin, APIView):
    @swagger_auto_schema(**RidiAccountInfoGetSchema.to_swagger_schema())
    def get(self, request):
        access_token = self.get_cookie(request=request, key=ACCESS_TOKEN_COOKIE_KEY)
        if access_token is None:
            code = self.make_response_code(ApiStatusCodes.C_401_UNAUTHORIZED, 'Not exist access_token')
            return self.fail_response(code)

        try:
            data = AccountInfoService.get_account_info(access_token)
        except ServerException:
            code = self.make_response_code(ApiStatusCodes.X_400_RIDIBOOKS_NOT_CONNECTION, 'Ridibooks server is not connected')
            return self.fail_response(code)
        except (HTTPException, InvalidResponseException):
            code = self.make_response_code(ApiStatusCodes.X_400_RIDIBOOKS_BAD_RESPONSE, 'Ridibooks server respond bad response')
            return self.fail_response(code)

        return self.success_response(data={'result': data['result']})
