from lib.base.constants import BaseConstant


class WorkerType(BaseConstant):
    STORE_USER_CRAWLER = 10
    _LIST = (STORE_USER_CRAWLER,)
    _STRING_MAP = {
        STORE_USER_CRAWLER: 'Store User Crawler'
    }
