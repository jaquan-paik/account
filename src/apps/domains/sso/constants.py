from lib.base.constants import BaseConstant

SSO_TOKEN_TTL = 60  # 60초


class SSOKeyHint(BaseConstant):
    VIEWER = 'viewer'

    _LIST = [VIEWER, ]
    _STRING_MAP = {
        VIEWER: '뷰어'
    }
