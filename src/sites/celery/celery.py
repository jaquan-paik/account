import os

from infra.configure.constants import SecretKeyName
from lib.secret.secret import Secret

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sites.celery.settings.' + Secret().get(SecretKeyName.ENVIRONMENT))

# noinspection PyUnresolvedReferences
from lib.celery.app import app as celery_app  # flake8: noqa: E402
