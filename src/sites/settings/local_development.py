from lib.log.setup import setup_logging

# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

setup_logging(Secret().get(SecretKeyName.SENTRY_DSN))

SITE_DOMAIN = 'account.dev.ridi.com'
ALLOWED_HOSTS = [SITE_DOMAIN, 'dev.ridi.com', ]

CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(\w+\.)?dev\.ridi\.com$',)

STORE_URL = 'http://login.dev.ridi.com'
RIDIBOOKS_LOGIN_URL = 'http://login.dev.ridi.com/account/login'

# django-debug-toolbar
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": 'lib.ridibooks.ip.utils.is_ridi_ip_from_request',
}

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE
