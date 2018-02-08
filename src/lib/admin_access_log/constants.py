from lib.base.constants import BaseConstant


class RequestMethod(BaseConstant):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3

    _LIST = (GET, POST, PUT, DELETE)
    _STRING_MAP = {
        GET: 'get',
        POST: 'post',
        PUT: 'put',
        DELETE: 'delete',
    }

    @classmethod
    def convert(cls, method: str) -> int:
        _method = method.upper()
        if _method == 'GET':
            return cls.GET
        if _method == 'POST':
            return cls.POST
        if _method == 'PUT':
            return cls.PUT
        if _method == 'DELETE':
            return cls.DELETE

        raise NotImplementedError
