from oauthlib.oauth2 import OAuth2Error

from infra.network.constants.http_status_code import HttpStatusCodes


class JwtTokenErrorException(Exception):
    pass


class FailOAuth2Exception(Exception):
    pass


class UnsupportedGrantType(OAuth2Error):
    error = 'unsupported_grant_type'
    status_code = HttpStatusCodes.C_400_BAD_REQUEST
    description = 'this grant type is not supported'


class DisallowedGrantType(OAuth2Error):
    error = 'disallowed_grant_type'
    status_code = HttpStatusCodes.C_400_BAD_REQUEST
    description = 'this grant type is disallowed'


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


class NotExistedClient(InvalidClient):
    description = 'this client is not existed'


class NotInHouseClient(InvalidClient):
    status_code = HttpStatusCodes.C_403_FORBIDDEN
    description = 'this client is not in-house client'


class InvalidRedirectUri(OAuth2Error):
    error = 'invalid_redirect_uri'
    status_code = HttpStatusCodes.C_403_FORBIDDEN
    description = 'this client is not authorized to use this redirect uri'


class InvalidAuthorizationGrantType(OAuth2Error):
    error = 'invalid_authorization_grant_type'
    status_code = HttpStatusCodes.C_403_FORBIDDEN
    description = 'this client is not authorized to use this authorization grant type.'


class InvalidClientSecret(OAuth2Error):
    error = 'invalid_client_secret'
    status_code = HttpStatusCodes.C_403_FORBIDDEN
    description = 'this secret is different with client\'s secret'


class InvalidClientType(OAuth2Error):
    error = 'invalid_client_type'
    status_code = HttpStatusCodes.C_403_FORBIDDEN
    description = 'this client is not authorized to use a grant type'


class MissingClientId(OAuth2Error):
    error = 'missing_client_id'
    status_code = HttpStatusCodes.C_400_BAD_REQUEST
    description = 'client id is required'


class MissingClientSecret(OAuth2Error):
    error = 'missing_client_secret'
    status_code = HttpStatusCodes.C_400_BAD_REQUEST
    description = 'client secret is required'


class MissingCode(OAuth2Error):
    error = 'missing_code'
    status_code = HttpStatusCodes.C_400_BAD_REQUEST
    description = 'code is required'


class MissingRedirectUri(OAuth2Error):
    error = 'missing_redirect_uri'
    status_code = HttpStatusCodes.C_400_BAD_REQUEST
    description = 'redirect uri is required'


class MissingRefreshToken(OAuth2Error):
    error = 'missing_refresh_token'
    status_code = HttpStatusCodes.C_400_BAD_REQUEST
    description = 'refresh token is required'


class MissingUsername(OAuth2Error):
    error = 'missing_username'
    status_code = HttpStatusCodes.C_400_BAD_REQUEST
    description = 'username is required'


class MissingGrantType(OAuth2Error):
    error = 'missing_grant_type'
    status_code = HttpStatusCodes.C_400_BAD_REQUEST
    description = 'grant type is required'
