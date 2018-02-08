from infra.configure.constants import SiteType

# noinspection PyUnresolvedReferences
from sites.base import *  # flake8: noqa: F403  # pylint:disable=wildcard-import

ROOT_URLCONF = 'sites.www.urls'
WSGI_APPLICATION = 'sites.www.wsgi.application'
SITE = SiteType.WWW
ALLOWED_HOSTS = [Secret().get(SecretKeyName.WWW_DOMAIN), ]
