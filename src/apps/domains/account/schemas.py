from drf_yasg import openapi
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
