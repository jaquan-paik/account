from infra.configure.constants import SiteType

# noinspection PyUnresolvedReferences
from sites.base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

ROOT_URLCONF = 'sites.admin.urls'
WSGI_APPLICATION = 'sites.admin.wsgi.application'
AUTH_USER_MODEL = 'account.Staff'
SITE = SiteType.ADMIN


MIDDLEWARE += [
    'lib.ridibooks.middlewares.RidiIPFilterMiddleware',
    'lib.admin_access_log.middlewares.AdminAccessLoggingMiddleware',
]

SESSION_COOKIE_AGE = 7200  # 60 * 60 * 2
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ALLOWED_HOSTS = [Secret().get(SecretKeyName.ADMIN_DOMAIN), ]
