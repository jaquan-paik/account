from infra.configure.constants import SiteType

# noinspection PyUnresolvedReferences
from sites.base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

MIDDLEWARE += [
    'lib.ridibooks.store_auth.middlewares.AuthenticationMiddleware',
]

ROOT_URLCONF = 'sites.www.urls'
WSGI_APPLICATION = 'sites.www.wsgi.application'
SITE = SiteType.WWW

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
