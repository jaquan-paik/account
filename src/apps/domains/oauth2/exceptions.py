from oauthlib.oauth2 import OAuth2Error

from infra.network.constants.http_status_code import HttpStatusCodes


class JwtTokenErrorException(Exception):
    pass


class LoginFailError(OAuth2Error):
    error = 'login_fail'
    status_code = HttpStatusCodes.C_401_UNAUTHORIZED
    description = 'Login failed'


class InvalidUserError(OAuth2Error):
    error = 'invalid_user'
    status_code = HttpStatusCodes.C_401_UNAUTHORIZED
    description = 'Authentication failed.'


class InvalidUserUnverifiedError(InvalidUserError):
    description = 'This account has not been verified.'


class InvalidUserSecededError(InvalidUserError):
    description = 'This account is unsubscribed.'


class InvalidUserDormantedError(InvalidUserError):
    description = 'This account is Inactive.'


class InvalidClient(OAuth2Error):
    error = 'invalid_client'
    status_code = HttpStatusCodes.C_401_UNAUTHORIZED
    description = 'invalid client'


class UnknownClient(InvalidClient):
    description = 'this client is unknown client'


class UnauthorizedClient(InvalidClient):
    error = 'unauthorized_client'
    description = 'this client is not authorized to use this authorization grant type.'


class NotInHouseClient(InvalidClient):
    status_code = HttpStatusCodes.C_403_FORBIDDEN
    description = 'this client is not in-house client'


class InvalidRedirectUri(InvalidClient):
    error = 'invalid_redirect_uri'
    status_code = HttpStatusCodes.C_403_FORBIDDEN
    description = 'this client can not use this redirect uri'
