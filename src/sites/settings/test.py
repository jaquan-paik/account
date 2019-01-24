# noinspection PyUnresolvedReferences
from sites.settings.base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

DATABASE_ROUTERS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'account-mariadb',
        'PORT': '3306',
        'CONN_MAX_AGE': 300,
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
            'charset': 'utf8',
        }
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

SITE_DOMAIN = 'account.ridibooks.com'
ALLOWED_HOSTS = [SITE_DOMAIN, 'dev.ridi.com', ]

STORE_URL = 'http://login.dev.ridi.com'
RIDIBOOKS_LOGIN_URL = 'http://login.dev.ridi.com/account/login'
COOKIE_ROOT_DOMAIN = '.ridibooks.com'
