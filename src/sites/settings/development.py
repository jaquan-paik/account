# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
