

class RootException(Exception):
    msg = ''

    def __init__(self, msg: str=''):
        super().__init__()
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class MsgException(RootException):
    pass


class ErrorException(RootException):
    pass
