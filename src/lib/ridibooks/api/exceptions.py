from lib.ridibooks.common.exceptions import RidibooksException


class InvalidRequestException(RidibooksException):
    pass


class InvalidUserException(RidibooksException):
    pass


class InvalidUserUnauthorizedException(InvalidUserException):
    pass


class InvalidUserUnverifiedException(InvalidUserException):
    pass


class InvalidUserSecededException(InvalidUserException):
    pass


class InvalidUserDormantedException(InvalidUserException):
    pass


class InvalidUserUnmatchedPasswordException(InvalidUserException):
    pass


class InvalidUserNotFoundException(InvalidUserException):
    pass


class StoreInternalServerErrorException(RidibooksException):
    pass
