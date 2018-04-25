
class RidibooksException(Exception):
    pass


class NotEnoughArgumentsException(RidibooksException):
    pass


class ServerException(RidibooksException):
    pass


class HTTPException(RidibooksException):
    def __init__(self, origin_exception, content, status):
        super().__init__()
        self.origin_exception = origin_exception
        self.content = content
        self.status = status

    def __str__(self):
        return f'[{self.status}] {str(self.origin_exception)}'


class InvalidResponseException(RidibooksException):
    pass
