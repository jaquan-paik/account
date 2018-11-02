from lib.base.constants import BaseConstant


class SecretEnvironment(BaseConstant):
    DEV = 'development'
    STAGING = 'staging'
    PROD = 'production'

    _LIST = (DEV, STAGING, PROD,)
    _STRING_MAP = {
        DEV: 'account_dev',
        STAGING: 'account_staging',
        PROD: 'account'
    }
