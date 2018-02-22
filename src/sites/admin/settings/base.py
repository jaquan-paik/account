from infra.configure.constants import SiteType

# noinspection PyUnresolvedReferences
from sites.base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

ROOT_URLCONF = 'sites.admin.urls'
WSGI_APPLICATION = 'sites.admin.wsgi.application'
AUTH_USER_MODEL = 'account_app.Staff'
SITE = SiteType.ADMIN


MIDDLEWARE += [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'lib.ridibooks.middlewares.RidiIPFilterMiddleware',
    'lib.admin_access_log.middlewares.AdminAccessLoggingMiddleware',
]

SESSION_COOKIE_AGE = 7200  # 60 * 60 * 2
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ALLOWED_HOSTS = ['account-admin.ridibooks.com', 'account-admin.dev.ridi.com', ]
