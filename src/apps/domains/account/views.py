from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from rest_framework.views import APIView

from apps.domains.account.services.account_info_service import AccountInfoService
from infra.configure.config import GeneralConfig
from infra.network.constants.api_status_code import ApiStatusCodes, StatusCode
from lib.base.exceptions import ErrorException
from lib.django.views.api.mixins import ResponseMixin
from lib.django.views.cookie.mixins import CookieMixin
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY
from lib.ridibooks.common.exceptions import HTTPException, InvalidResponseException, ServerException
from lib.utils.url import generate_query_url


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

            redirect_to = generate_query_url(GeneralConfig.get_ridibooks_login_url(), params)

        return HttpResponseRedirect(redirect_to)

    def post(self, request, *args, **kwargs):
        # 로그인 기능이 없기 때문에 막아둔다.
        pass

    def put(self, *args, **kwargs):
        # 로그인 기능이 없기 때문에 막아둔다.
        pass


class RidiAccountInfoView(CookieMixin, ResponseMixin, APIView):
    def get(self, request):
        access_token = self.get_cookie(request=request, key=ACCESS_TOKEN_COOKIE_KEY)
        if access_token is None:
            code = self.make_response_code(ApiStatusCodes.C_401_UNAUTHORIZED)
            return self.fail_response(response_code=code)
        try:
            data = AccountInfoService.get_account_info(access_token=access_token)
        except (InvalidResponseException, ServerException):
            code = self.make_response_code(ApiStatusCodes.C_504_GATEWAY_TIMEOUT)
            return self.fail_response(response_code=code)
        except HTTPException as e:
            code = self.make_response_code(StatusCode(status=e.status))
            return self.fail_response(code)

        code = self.make_response_code(status=ApiStatusCodes.C_200_OK)
        return self.success_response(data=data, response_code=code)
