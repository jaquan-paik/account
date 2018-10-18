from drf_yasg import openapi
from lib.base.schema import BaseSchema, SecurityScope


class TokenGetSchema(BaseSchema):
    operation_id = '토큰 refresh'
    operation_description = '토큰 발급 혹은 토큰 refresh'
    security_scope = SecurityScope.PUBLIC
    manual_parameters = [openapi.Parameter(
        in_='cookie',
        name='ridi_rt',
        type='oauth2',
        description='Refresh Token'
    )]
    responses = {
        '200': openapi.Response(
            description='set ridi-rt, ridi-at in the cookie',
            examples={
                "expires_at": "2016-10-27T17:13:40+00:00",
                "expires_in": 3600
            },
            headers={
                "Set-Cookie": {
                    "description": '- ridi-at=abcde12345; Path=/; Domain=ridibooks.com; Secure; HttpOnly \n'
                                   '- ridi-rt=abcde12345; Path=/; Domain=ridibooks.com; Secure; HttpOnly',
                    "schema": {
                        'type': 'string'
                    }
                }
            }
        ),
        '403': openapi.Response(
            description='invalid_request'
        )
    }
