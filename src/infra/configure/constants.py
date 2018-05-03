class SiteType:
    ADMIN = 'admin'
    WWW = 'www'
    CELERY = 'celery'
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

    CELERY_BROKER_URL = 'celery_broker_url'

    OAUTH2_ACCESS_JWT_SECRET = 'oauth2_access_jwt_secret'

    RIDI_CMS_RPC_URL = "ridi_cms_rpc_url"
