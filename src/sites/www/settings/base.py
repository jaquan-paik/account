from infra.configure.constants import SiteType

# noinspection PyUnresolvedReferences
from sites.base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

MIDDLEWARE += [
    'lib.ridibooks.middlewares.AuthenticationMiddleware',
]

ROOT_URLCONF = 'sites.www.urls'
WSGI_APPLICATION = 'sites.www.wsgi.application'
SITE = SiteType.WWW
ALLOWED_HOSTS = [Secret().get(SecretKeyName.WWW_DOMAIN), ]


LOGIN_URL = 'https://ridibooks.com/account/login?return_url=https%3A%2F%2Faccount.ridibooks.com'
