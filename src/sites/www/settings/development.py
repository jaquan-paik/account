from infra.configure.constants import LogLevel
from lib.log.setup import setup_logging

# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

setup_logging(SITE, LogLevel.DEBUG, LOG_DIR)

SITE_DOMAIN = 'account.ridibooks.com'
ROOT_DOMAIN = 'ridibooks.com'
ALLOWED_HOSTS = [SITE_DOMAIN, ]


# django-debug-toolbar
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": 'lib.ridibooks.utils.is_ridi_ip_from_request',
}

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE
