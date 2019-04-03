from lib.base.constants import BaseConstant

# pyJWT 라이브러리의 leeway 값은 토큰의 유효기간을 늘려주는 값이다.
JWT_VERIFY_MARGIN = -(60 * 10)  # -10분

GRANT_CODE_LENGTH = 30
DEFAULT_SCOPE = 'all'

TOKEN_TYPE = 'Bearer'

# AccessToken
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60  # 3600, 1hour

# RefershToken
REFRESH_TOKEN_EXPIRE_SECONDS = 30 * 24 * 60 * 60  # 2592000, 30 days
REFRESH_TOKEN_EXPIRE_DAYS = 30


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
    OLD_AUTHORIZATION_CODE = 'authorization-code'  # 호환성을 위해 필요하지만 후에 제거 되어야한다.

    _LIST = [AUTHORIZATION_CODE, PASSWORD, CLIENT_CREDENTIALS, REFRESH_TOKEN, OLD_AUTHORIZATION_CODE]


class ResponseType:
    CODE = 'code'
