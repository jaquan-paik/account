from lib.base.constants import BaseConstant

SSO_TOKEN_TTL = 60  # 60초


class SSOKeyHint(BaseConstant):
    VIEWER = 'viewer'
    SESSION_LOGIN = 'session_login'

    _LIST = [VIEWER, SESSION_LOGIN]
    _STRING_MAP = {
        VIEWER: '뷰어',
        SESSION_LOGIN: '스토어 세션 로그인'
    }
