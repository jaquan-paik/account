from lib.base.constants import BaseConstant

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
