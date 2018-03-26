from infra.configure.constants import LogLevel
from lib.log.setup import setup_logging

# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

setup_logging(LogLevel.DEBUG)

# Sentry
RAVEN_CONFIG = {
    'dsn': Secret().get(SecretKeyName.SENTRY_DSN),
    'release': '',
    'ignore_exceptions': [
        'django.exceptions.http.Http404',
        'common.exceptions.MsgException',
    ],
}

SITE_DOMAIN = 'account.ridibooks.com'
ROOT_DOMAIN = 'ridibooks.com'
ALLOWED_HOSTS = [SITE_DOMAIN, ]
