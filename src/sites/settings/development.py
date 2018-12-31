from lib.log.setup import setup_logging

# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

setup_logging(Secret().get(SecretKeyName.SENTRY_DSN))

SITE_DOMAIN = Secret().get(SecretKeyName.SITE_DOMAIN)

ALLOWED_HOSTS = Secret().get(SecretKeyName.ALLOWED_HOSTS)

STORE_URL = Secret().get(SecretKeyName.STORE_URL)

RIDIBOOKS_LOGIN_URL = Secret().get(SecretKeyName.RIDIBOOKS_LOGIN_URL)

CORS_ORIGIN_REGEX_WHITELIST = (
    r'^(https?:\/\/)?(.+\.)?ridi\.io$',
)
# django-debug-toolbar
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": 'lib.ridibooks.ip.utils.is_ridi_ip_from_request',
}

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE
