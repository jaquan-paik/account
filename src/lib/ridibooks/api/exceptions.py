class RidibooksException(Exception):
    pass


class NotEnoughArgumentsException(RidibooksException):
    pass


class RequestFailException(RidibooksException):
    pass


class InvalidResponseException(RidibooksException):
    pass
