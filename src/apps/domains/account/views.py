from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from ridi_django_oauth2.decorators import scope_required
from ridi_oauth2.resource.constants import Scope

from apps.domains.account.repositories import UserModifiedHistoryRepository, UserRepository
from apps.domains.account.schemas import MultipleUserInfoPostSchema, RidiAccountInfoGetSchema, UserModifiedHistoryGetSchema
from apps.domains.account.serializers import MultipleUserRequestSerializer, MultipleUserResponseSerializer, \
    UserModifiedHistoryRequestSerializer, UserModifiedHistoryResponseSerializer
from apps.domains.account.services.account_info_service import AccountInfoService
from infra.configure.config import GeneralConfig
from infra.network.constants.api_status_code import ApiStatusCodes
from lib.base.exceptions import ErrorException
from lib.decorators.ridi_oauth2_access_token_login import ridi_oauth2_access_token_login
from lib.decorators.session_login import ridibooks_session_login
from lib.django.views.api.mixins import ResponseMixin
from lib.django.views.cookie.mixins import CookieMixin
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY
from lib.ridibooks.common.exceptions import HTTPException, InvalidResponseException, ServerException
from lib.ridibooks.internal_server_auth.decorators import ridi_internal_auth
from lib.utils.url import generate_query_url


class RidiLoginView(LoginView):  # pylint: disable=too-many-ancestors
    @ridibooks_session_login()
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


@method_decorator(ridi_oauth2_access_token_login, 'dispatch')
class RidiAccountInfoView(CookieMixin, ResponseMixin, APIView):
    @swagger_auto_schema(**RidiAccountInfoGetSchema.to_swagger_schema())
    @scope_required(required_scopes=[Scope.ALL])
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

        except InvalidResponseException:
            code = self.make_response_code(ApiStatusCodes.X_400_RIDIBOOKS_BAD_RESPONSE, 'Ridibooks server respond bad response')
            return self.fail_response(code)

        except HTTPException as e:
            if e.status == ApiStatusCodes.C_401_UNAUTHORIZED:
                code = self.make_response_code(ApiStatusCodes.C_401_UNAUTHORIZED)
            else:
                code = self.make_response_code(ApiStatusCodes.X_400_RIDIBOOKS_BAD_RESPONSE, 'Ridibooks server respond bad response')

            return self.fail_response(code)

        return self.success_response(data={'result': data['result']})


@method_decorator(ridi_internal_auth, 'dispatch')
class UserInfoView(ResponseMixin, APIView):
    @swagger_auto_schema(**MultipleUserInfoPostSchema.to_swagger_schema())
    def post(self, request):
        serializer = MultipleUserRequestSerializer(data=request.data)
        if not serializer.is_valid():
            code = self.make_response_code(ApiStatusCodes.C_400_BAD_REQUEST)
            return self.fail_response(response_code=code, data=serializer.errors)

        users = UserRepository.find_by_u_idxes(serializer.validated_data['u_idxes'])
        return self.success_response(data=MultipleUserResponseSerializer(
            {'users': users}, fields={'users': serializer.validated_data['fields']}
        ).data)


@method_decorator(ridi_internal_auth, 'dispatch')
class UserModifiedHistoryView(ResponseMixin, APIView):
    @swagger_auto_schema(**UserModifiedHistoryGetSchema.to_swagger_schema())
    def get(self, request):
        serializer = UserModifiedHistoryRequestSerializer(data=request.data)
        if not serializer.is_valid():
            code = self.make_response_code(ApiStatusCodes.C_400_BAD_REQUEST)
            return self.fail_response(response_code=code, data=serializer.errors)

        order = serializer.validated_data['order']
        offset = serializer.validated_data['offset']
        limit = serializer.validated_data['limit']

        histories = UserModifiedHistoryRepository.find_order_or_over(order, offset, limit)
        return self.success_response(data=UserModifiedHistoryResponseSerializer({'histories': histories}).data)
