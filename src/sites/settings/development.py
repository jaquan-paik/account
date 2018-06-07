from lib.log.setup import setup_logging

# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

setup_logging()

SITE_DOMAIN = 'account.dev.ridi.io'
ALLOWED_HOSTS = [SITE_DOMAIN, 'account.dev.ridi.com', 'dev.ridi.com', 'dev.ridi.io']

CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(\w+\.)?dev\.ridi\.com$', r'^(https?://)?(\w+\.)?dev\.ridi\.io$')
CORS_URLS_REGEX = r'^/ridi/.*$'

RIDIBOOKS_LOGIN_URL = 'https://dev.ridi.io/account/login'


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
