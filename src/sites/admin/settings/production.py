from lib.log.setup import setup_logging

# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

# noinspection PyUnresolvedReferences
setup_logging()

SITE_DOMAIN = 'admin.ridibooks.com'
ALLOWED_HOSTS = [SITE_DOMAIN, ]
