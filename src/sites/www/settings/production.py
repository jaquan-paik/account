from lib.log.setup import setup_logging

# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

# noinspection PyUnresolvedReferences
setup_logging(DEBUG)

SITE_DOMAIN = 'account.ridibooks.com'

# noinspection PyUnresolvedReferences
ALLOWED_HOSTS = [SITE_DOMAIN, 'ridibooks.com']
