from lib.log.setup import setup_logging

# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

# noinspection PyUnresolvedReferences
setup_logging(DEBUG)

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
