from infra.network.constants.http_status_code import HttpStatusCodes
from lib.base.constants import BaseConstant

# pyJWT 라이브러리의 leeway 값은 토큰의 유효기간을 늘려주는 값이다.
JWT_VERIFY_MARGIN = -(60 * 10)  # -10분
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60  # 3600, 1hour
CODE_LENGTH = 30
SCOPE = 'all'


class JwtAlg(BaseConstant):
    HS256 = 'HS256'
    RS256 = 'RS256'

    _LIST = [HS256, RS256, ]
    _STRING_MAP = {
        HS256: 'HS256',
        RS256: 'RS256',
    }


class GrantType(BaseConstant):
    AUTHORIZATION_CODE = 'authorization_code'
    PASSWORD = 'password'
    CLIENT_CREDENTIALS = 'client_credentials'
    REFRESH_TOKEN = 'refresh_token'

    _LIST = [AUTHORIZATION_CODE, PASSWORD, CLIENT_CREDENTIALS, REFRESH_TOKEN]


class ResponseType:
    CODE = 'code'


class ErrorMessage(BaseConstant):
    REQUIRED_CLIENT_ID = 'required_client_id'
    UNSUPPORTED_RESPONSE_TYPE = 'unsupported_response_type'
    REQUIRED_RESPONSE_TYPE = 'required_response_type'
    REQUIRED_REDIRECT_URI = 'required_redirect_uri'

    _LIST = [REQUIRED_CLIENT_ID, UNSUPPORTED_RESPONSE_TYPE, REQUIRED_RESPONSE_TYPE, REQUIRED_REDIRECT_URI]
    _INT_MAP = {
        REQUIRED_CLIENT_ID: HttpStatusCodes.C_500_INTERNAL_SERVER_ERROR,
        UNSUPPORTED_RESPONSE_TYPE: HttpStatusCodes.C_400_BAD_REQUEST,
        REQUIRED_RESPONSE_TYPE: HttpStatusCodes.C_400_BAD_REQUEST,
        REQUIRED_REDIRECT_URI: HttpStatusCodes.C_400_BAD_REQUEST
    }

    @classmethod
    def get_code_from_error_message(cls, code):
        return cls._INT_MAP.get(code, HttpStatusCodes.C_400_BAD_REQUEST)
