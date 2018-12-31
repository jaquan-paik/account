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


class SecretKeyName:
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
