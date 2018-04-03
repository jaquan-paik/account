from infra.configure.constants import SiteType
# noinspection PyUnresolvedReferences
from sites.base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

DATABASE_ROUTER = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
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
