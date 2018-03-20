from infra.configure.constants import SiteType
from lib.celery.app import generate_celery

celery_app = generate_celery(SiteType.CELERY)
