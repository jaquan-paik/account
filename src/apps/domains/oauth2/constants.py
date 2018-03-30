from lib.base.constants import BaseConstant


JWT_VERIFY_MARGIN = 60 * 10  # 10분


class JwtAlg(BaseConstant):
    HS256 = 'HS256'
    RS256 = 'RS256'

    _LIST = [HS256, RS256, ]
    _STRING_MAP = {
        HS256: 'HS256',
        RS256: 'RS256',
    }


APPLICATION_CACHE_TTL = 60 * 60
REFRESH_TOKEN_CACHE_TTL = 60 * 5
