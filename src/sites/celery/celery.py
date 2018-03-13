import os

from infra.configure.constants import SecretKeyName, SiteType
from lib.secret.secret import Secret
from lib.celery.app import generate_celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sites.celery.settings.' + Secret().get(SecretKeyName.ENVIRONMENT))

celery_app = generate_celery(SiteType.CELERY)
