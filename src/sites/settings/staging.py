from lib.log.setup import setup_logging

# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

setup_logging(Secret().get(SecretKeyName.SENTRY_DSN))

SITE_DOMAIN = 'account.ridibooks.com'
ALLOWED_HOSTS = [
    SITE_DOMAIN,
    'ridibooks.com',
    'ezwel.ridibooks.com'
]

STORE_URL = 'https://ridibooks.com'
RIDIBOOKS_LOGIN_URL = 'https://ridibooks.com/account/login'

CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(\w+\.)?ridibooks\.com$',)
