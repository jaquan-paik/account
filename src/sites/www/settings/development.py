from infra.configure.constants import LogLevel
from lib.log.setup import setup_logging

# noinspection PyUnresolvedReferences
from .base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

setup_logging(SITE, LogLevel.DEBUG, LOG_DIR)
