import os

from apps.domains.sso.constants import SSOKeyHint
from infra.configure.constants import SecretKeyName
from lib.log.setup import setup_logging
from lib.ridibooks.internal_server_auth.helpers.config_helper import AuthList, ConfigHelper as InternalServerAuthConfigHelper
from lib.secret.secret import Secret
from lib.settings.asserts import assert_allowed_hosts_with_cookie_root_domain

# PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # src dir

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Secret().get(SecretKeyName.SECRET_KEY)

ENVIRONMENT = Secret().get(SecretKeyName.ENVIRONMENT)

setup_logging(Secret().get(SecretKeyName.SENTRY_DSN))

SITE_DOMAIN = Secret().get(SecretKeyName.SITE_DOMAIN)

ALLOWED_HOSTS = Secret().get(SecretKeyName.ALLOWED_HOSTS).split()

STORE_URL = Secret().get(SecretKeyName.STORE_URL)

STORE_API_URL = Secret().get(SecretKeyName.STORE_API_URL)

RIDIBOOKS_LOGIN_URL = Secret().get(SecretKeyName.RIDIBOOKS_LOGIN_URL)

CORS_ORIGIN_REGEX_WHITELIST = (rf"{Secret().get(SecretKeyName.CORS_ORIGIN_REGEX_WHITELIST)}",)

COOKIE_ROOT_DOMAIN = Secret().get(SecretKeyName.COOKIE_ROOT_DOMAIN)

# allowed hosts 안에 있는 호스트 들은 쿠키 루트 도메인으로 이루어져있음을 보장해야한다.
assert_allowed_hosts_with_cookie_root_domain(ALLOWED_HOSTS, COOKIE_ROOT_DOMAIN)

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

    'ridi_django_oauth2',

    # django api 문서화 라이브러리
    'drf_yasg',

    # custom
    'lib.django.apps.DjangoAppConfig',

    # logging
    'raven.contrib.django.raven_compat',

    # app
    'apps.domains.account.apps.AccountConfig',
    'apps.domains.oauth2.apps.OAuth2Config',
    'apps.domains.ridi.apps.RidiConfig',
    'apps.domains.sso.apps.SSOAppConfig',
    # routines
    'apps.globals.routines.worker_status.apps.WorkerStatusAppConfig',
]

MIDDLEWARE = [
    'lib.health_check.middlewares.HealthCheckerMiddleware',
    'lib.django.middlewares.smart_append_slash_middleware.SmartAppendSlashMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
        'CONN_MAX_AGE': 0,
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

# RIDI Django OAuth2 Setting
RIDI_OAUTH2_CLIENT_ID = Secret().get(SecretKeyName.RIDI_CLIENT_ID)
RIDI_OAUTH2_CLIENT_SECRET = Secret().get(SecretKeyName.RIDI_CLIENT_SECRET)
RIDI_OAUTH2_JWT_SECRET = Secret().get(SecretKeyName.RIDI_JWT_SECRET)

# RIDI Internal Server Auth
RIDI_INTERNAL_AUTH_DATA = InternalServerAuthConfigHelper.generate_auth_data({
    AuthList.ACCOUNT_TO_STORE: Secret().get(SecretKeyName.RIDI_INTERNAL_AUTH_ACCOUNT_TO_STORE),
})

RIDI_INTERNAL_AUTH_REQUIRE_EXP = False

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r'^/(ridi|oauth2|health|accounts)/.*$'

# Sentry
RAVEN_CONFIG = {
    'dsn': Secret().get(SecretKeyName.SENTRY_DSN),
    'release': '',
    'ignore_exceptions': [
        'django.exceptions.http.Http404',
        'lib.base.exceptions.MsgException',
        'OSError',
    ],
    'exclude_paths': [
        'ridi_django_oauth2',
        'rest_framework',
    ],
}

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'ridi_django_oauth2.rest_framework.authentication.OAuth2Authentication',
    ),
}

STATE_CRYPTO_KEY = Secret().get(SecretKeyName.STATE_CRYPTO_KEY)

SSO_CRYPTO_KEYS = {
    SSOKeyHint.VIEWER: Secret().get(SecretKeyName.SSO_KEY_VIEWER)
}