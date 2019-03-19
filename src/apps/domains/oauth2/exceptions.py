from oauthlib.oauth2 import OAuth2Error


class JwtTokenErrorException(Exception):
    pass


class LoginFailError(OAuth2Error):
    error = 'login_fail'
    status_code = 401
    description = 'Login failed'


class InvalidUserError(OAuth2Error):
    error = 'invalid_user'
    status_code = 401
    description = 'Authentication failed.'


class InvalidUserUnverifiedError(InvalidUserError):
    description = 'This account has not been verified.'


class InvalidUserSecededError(InvalidUserError):
    description = 'This account is unsubscribed.'


class InvalidUserDormantedError(InvalidUserError):
    description = 'This account is Inactive.'
