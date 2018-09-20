from oauthlib.oauth2 import OAuth2Error


class JwtTokenErrorException(Exception):
    pass


class LoginFailError(OAuth2Error):
    error = 'login_fail'
    status_code = 401
    description = '로그인에 실패했습니다.'


class InvalidUserError(OAuth2Error):
    error = 'invalid_user'
    status_code = 401
    description = '인증에 실패했습니다.'


class InvalidUserUnverifiedError(InvalidUserError):
    description = '인증이 완료되지 않은 계정입니다.'


class InvalidUserSecededError(InvalidUserError):
    description = '탈퇴된 계정입니다.'


class InvalidUserDormantedError(InvalidUserError):
    description = '휴면 계정입니다.'
