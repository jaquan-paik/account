import os

from infra.configure.constants import SecretKeyName
from infra.storage.redis.constants import RedisDatabase
from lib.secret.secret import Secret

# PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # src dir
ROOT_DIR = os.path.dirname(BASE_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Secret().get(SecretKeyName.SECRET_KEY)

ENVIRONMENT = Secret().get(SecretKeyName.ENVIRONMENT)

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lib.email.apps.EmailConfig',
    'rest_framework',

    # django api 문서화 라이브러리
    'drf_yasg',

    # security
    'lib.admin_access_log.apps.AdminAccessLogConfig',

    # custom
    'lib.django.apps.DjangoAppConfig',

    # logging
    'raven.contrib.django.raven_compat',

    # app
    'apps.domains.account.apps.AccountConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# session
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_SOCKET_TIMEOUT = 1

SESSION_REDIS = {
    'host': Secret().get(SecretKeyName.REDIS_HOST),
    'port': 6379,
    'db': RedisDatabase.SESSION,
    'prefix': 'session',
    'socket_timeout': 1
}


DATABASE_ROUTERS = ['infra.storage.database.routers.DbRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': Secret().get(SecretKeyName.WRITE_DB_ACCOUNT),
        'PASSWORD': Secret().get(SecretKeyName.WRITE_DB_PASSWORD),
        'HOST': Secret().get(SecretKeyName.WRITE_DB_HOST),
        'PORT': '3306',
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
            'charset': 'utf8',
        }
    },
    'write': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': Secret().get(SecretKeyName.WRITE_DB_ACCOUNT),
        'PASSWORD': Secret().get(SecretKeyName.WRITE_DB_PASSWORD),
        'HOST': Secret().get(SecretKeyName.WRITE_DB_HOST),
        'PORT': '3306',
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
            'charset': 'utf8',
        }
    },
    'read': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': Secret().get(SecretKeyName.READ_DB_ACCOUNT),
        'PASSWORD': Secret().get(SecretKeyName.READ_DB_PASSWORD),
        'HOST': Secret().get(SecretKeyName.READ_DB_HOST),
        'PORT': '3306',
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
            'charset': 'utf8',
        }
    },
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': Secret().get(SecretKeyName.MEMCACHED_LOCATION),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

ENFORCE_TWO_FACTOR_AUTH = False

# Logging
IGNORE_404_FILTER_URLS = []
LOGGING_CONFIG = None
LOG_DIR = os.path.join(ROOT_DIR, 'logs')


AUTH_USER_MODEL = 'account.User'


# celery setting
CELERY_BROKER_URL = Secret().get(SecretKeyName.CELERY_BROKER_URL)
CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_ENABLE_UTC = True
CELERY_IMPORTS = [
]

CORS_ORIGIN_ALLOW_ALL = True


OAUTH2_ACCESS_JWT_SECRET = Secret().get(SecretKeyName.OAUTH2_ACCESS_JWT_SECRET)
