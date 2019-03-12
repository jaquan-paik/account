from lib.base.constants import BaseConstant

ACCESS_TOKEN_COOKIE_KEY = 'ridi-at'
REFRESH_TOKEN_COOKIE_KEY = 'ridi-rt'
AUTO_LOGIN_COOKIE_KEY = 'ridi-al'
AUTO_LOGIN_ON_COOKIE_VALUE = '1'
PHP_SESSION_COOKIE_KEY = 'PHPSESSID'

HTTP_AUTHORIZATION_HEADER = 'HTTP_AUTHORIZATION'


class HttpMethod(BaseConstant):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 4

    _LIST = [GET, POST, PUT, DELETE]
    _STRING_MAP = {
        GET: 'GET',
        POST: 'POST',
        PUT: 'PUT',
        DELETE: 'DELETE'
    }
