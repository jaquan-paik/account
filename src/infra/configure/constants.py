from lib.base.constants import BaseConstant


class SiteType:
    WWW = 'www'
    TEST = 'test'


class LogLevel:
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    NOTSET = 'NOTSET'


class SecretKeyName(BaseConstant):
    # static member
    ENVIRONMENT = 'environment'

    SECRET_KEY = 'secret_key'

    CACHE_LOCATION = 'cache_location'

    WRITE_DB_HOST = 'write_db_host'
    WRITE_DB_ACCOUNT = 'write_db_account'
    WRITE_DB_PASSWORD = 'write_db_password'

    READ_DB_HOST = 'read_db_host'
    READ_DB_ACCOUNT = 'read_db_account'
    READ_DB_PASSWORD = 'read_db_password'

    REDIS_HOST = 'redis_host'

    SENTRY_DSN = 'sentry_dsn'

    RIDI_INTERNAL_AUTH_ACCOUNT_TO_STORE = 'ridi_internal_auth_account_to_store'

    STATE_CRYPTO_KEY = 'state_crypto_key'

    SITE_DOMAIN = 'site_domain'
    STORE_URL = 'store_url'
    RIDIBOOKS_LOGIN_URL = 'ridibooks_login_url'
    ALLOWED_HOSTS = 'allowed_hosts'
    CORS_ORIGIN_REGEX_WHITELIST = 'cors_origin_regex_whitelist'
    IN_HOUSE_CLIENT_REDIRECT_URI_REGEX = 'in_house_client_redirect_uri_regex'

    _LIST = [
        ENVIRONMENT, SECRET_KEY, CACHE_LOCATION, WRITE_DB_HOST, WRITE_DB_ACCOUNT, WRITE_DB_PASSWORD, READ_DB_HOST, READ_DB_ACCOUNT,
        READ_DB_PASSWORD, REDIS_HOST, SENTRY_DSN, RIDI_INTERNAL_AUTH_ACCOUNT_TO_STORE, STATE_CRYPTO_KEY, SITE_DOMAIN, STORE_URL,
        RIDIBOOKS_LOGIN_URL, ALLOWED_HOSTS, CORS_ORIGIN_REGEX_WHITELIST
    ]
