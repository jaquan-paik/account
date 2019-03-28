from drf_yasg import openapi

from apps.domains.account.serializers import MultipleUserRequestSerializer, MultipleUserResponseSerializer, \
    UserModifiedHistoryRequestSerializer, UserModifiedHistoryResponseSerializer
from lib.base.schema import BaseSchema, SecurityScope


class RidiAccountInfoGetSchema(BaseSchema):
    operation_id = 'store api에서 유저 데이터 가져오기'
    operation_description = 'cookie에서 ridi_at 확인 후 정보 가저오기'
    security_scope = SecurityScope.PUBLIC
    responses = {
        '200': openapi.Response(
            'success', examples={'result': 'user object'}
        ),
        '401': openapi.Response(
            description='Not exist access_token'
        ),
        '400': openapi.Response(
            description='Ridibooks server is not connected or Ridibooks server respond bad response'
        )
    }


class MultipleUserInfoPostSchema(BaseSchema):
    operation_id = 'Multiple user info'
    operation_description = '유저 리스트'
    request_body = MultipleUserRequestSerializer
    security_scope = SecurityScope.INTERNAL
    responses = {
        '200': openapi.Response('success', schema=MultipleUserResponseSerializer(), )
    }


class UserModifiedHistoryGetSchema(BaseSchema):
    operation_id = 'User modified history'
    operation_description = '사용자 정보 변경 리스트'
    query_serializer = UserModifiedHistoryRequestSerializer
    security_scope = SecurityScope.INTERNAL
    responses = {
        '200': openapi.Response('success', schema=UserModifiedHistoryResponseSerializer(), )
    }
