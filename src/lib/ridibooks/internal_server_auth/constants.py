from lib.base.constants import BaseConstant

DEFAULT_ALG = 'RS256'
DEFAULT_EXPIRE_MARGIN_MINS = 5


class Method:
    REQ = 'req'
    RES = 'res'


class ServiceList(BaseConstant):
    ACCOUNT = 'account'
    LIBRARY = 'library'
    USER_BOOK = 'user-book'
    BOOK = 'book'
    CPS = 'cps'
    SEARCH = 'search'
    STORE = 'store'


class AuthList(BaseConstant):
    USER_BOOK_TO_LIBRARY = f'{ServiceList.USER_BOOK}:{ServiceList.LIBRARY}'
    CPS_TO_LIBRARY = f'{ServiceList.CPS}:{ServiceList.LIBRARY}'

    LIBRARY_TO_BOOK = f'{ServiceList.LIBRARY}:{ServiceList.BOOK}'
    LIBRARY_TO_SEARCH = f'{ServiceList.LIBRARY}:{ServiceList.SEARCH}'

    ACCOUNT_TO_STORE = f'{ServiceList.ACCOUNT}:{ServiceList.STORE}'

    _LIST = (
        USER_BOOK_TO_LIBRARY, CPS_TO_LIBRARY,
        LIBRARY_TO_BOOK, LIBRARY_TO_SEARCH,
        ACCOUNT_TO_STORE,
    )
