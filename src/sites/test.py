from infra.configure.constants import SiteType
# noinspection PyUnresolvedReferences
from sites.base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

DATABASE_ROUTER = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': 'admin',
        'PASSWORD': 'test',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
            'charset': 'utf8',
        },
        'TEST': {
            'NAME': 'account',
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        }
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

SITE = SiteType.TEST
SITE_DOMAIN = 'account.ridibooks.com'
ALLOWED_HOSTS = [SITE_DOMAIN, 'dev.ridi.com', ]

MIDDLEWARE += [
    'lib.ridibooks.middlewares.AuthenticationMiddleware',
]
ROOT_URLCONF = 'sites.www.urls'
