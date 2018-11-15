import os

from infra.configure.constants import SecretKeyName
from infra.storage.redis.constants import RedisDatabase
from lib.ridibooks.internal_server_auth.helpers.config_helper import AuthList, ConfigHelper as InternalServerAuthConfigHelper
from lib.secret.secret import Secret

# PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # src dir

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Secret().get(SecretKeyName.SECRET_KEY)

ENVIRONMENT = Secret().get(SecretKeyName.ENVIRONMENT)

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'oauth2_provider',
    'corsheaders',

    # django api 문서화 라이브러리
    'drf_yasg',

    # custom
    'lib.django.apps.DjangoAppConfig',

    # logging
    'raven.contrib.django.raven_compat',

    # app
    'apps.domains.account.apps.AccountConfig',
    'apps.domains.oauth2.apps.OAuth2Config',
    'apps.domains.callback.apps.CallbackConfig',
]

MIDDLEWARE = [
    'lib.health_check.middlewares.HealthCheckerMiddleware',
    'lib.django.middlewares.smart_append_slash_middleware.SmartAppendSlashMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # TODO test
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'lib.ridibooks.store_auth.middlewares.AuthenticationMiddleware',
]

ROOT_URLCONF = 'sites.urls'
WSGI_APPLICATION = 'sites.wsgi.application'

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
DATABASE_ROUTERS = ['infra.storage.database.routers.DbRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': Secret().get(SecretKeyName.WRITE_DB_ACCOUNT),
        'PASSWORD': Secret().get(SecretKeyName.WRITE_DB_PASSWORD),
        'HOST': Secret().get(SecretKeyName.WRITE_DB_HOST),
        'PORT': '3306',
        'CONN_MAX_AGE': 300,
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
            'charset': 'utf8',
        }
    },
}

DATABASE_APPS_MAPPING = {
    'oauth2_app': 'account',
    'account_app': 'account',
}

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": Secret().get(SecretKeyName.CACHE_LOCATION),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
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


# Logging
IGNORE_404_FILTER_URLS = []
LOGGING_CONFIG = None

APPEND_SLASH = False

AUTH_USER_MODEL = 'account_app.User'


# Login
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'


# Session
SESSION_COOKIE_AGE = 60 * 12
SESSION_COOKIE_SECURE = True

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_SOCKET_TIMEOUT = 1

SESSION_REDIS = {
    'host': Secret().get(SecretKeyName.REDIS_HOST),
    'port': 6379,
    'db': RedisDatabase.SESSION,
    'prefix': 'session',
    'socket_timeout': 1
}


# OAuth2
OAUTH2_PROVIDER = {
    'SCOPES': {
        'all': 'All(for internal service)',
    },

    'OAUTH2_SERVER_CLASS': 'apps.domains.oauth2.server.RidiServer',
    'OAUTH2_VALIDATOR_CLASS': 'apps.domains.oauth2.oauth2_validators.RidiOAuth2Validator',

    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 60,  # 3600, 1hour
    'REFRESH_TOKEN_EXPIRE_SECONDS': 60 * 60 * 24 * 30,  # 2,592,000, 30days
    'ALLOWED_REDIRECT_URI_SCHEMES': ['https'],
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 60 * 10,  # 600 10min
    'ROTATE_REFRESH_TOKEN': True,
}

OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_app.Application'
OAUTH2_PROVIDER_GRANT_MODEL = 'oauth2_app.Grant'
OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = 'oauth2_app.AccessToken'
OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = 'oauth2_app.RefreshToken'

# TODO: 버그로 인해 해당 셋팅 추가. 버젼이 1.0.0 <  이 되면 제거
# https://github.com/evonove/django-oauth-toolkit/commit/65af7372a0fb208a19899fa75982163bdff713f9
OAUTH2_PROVIDER_REFRESH_MODEL = 'oauth2_app.RefreshToken'

# RIDI Internal Server Auth
RIDI_INTERNAL_AUTH_DATA = InternalServerAuthConfigHelper.generate_auth_data({
    AuthList.ACCOUNT_TO_STORE: Secret().get(SecretKeyName.RIDI_INTERNAL_AUTH_ACCOUNT_TO_STORE),
})

RIDI_INTERNAL_AUTH_REQUIRE_EXP = False

# Security
# TODO test
# X_FRAME_OPTIONS = 'ALLOW-FROM https://ez1.s-bluevery.com/'
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SAMESITE = None

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True

# TODO test
# CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r'^/(ridi|oauth2|health|accounts)/.*$'

ALLOWED_HOSTS = []


# Sentry
RAVEN_CONFIG = {
    'dsn': Secret().get(SecretKeyName.SENTRY_DSN),
    'release': '',
    'ignore_exceptions': [
        'django.exceptions.http.Http404',
        'lib.base.exceptions.MsgException',
        'OSError',
    ],
}

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (),
}
