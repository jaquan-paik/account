from celery.task import task
from django.core.management import call_command

from infra.celery.constants import CeleryQueue


@task(queue=CeleryQueue.LOW,)
def revoke_expired_tokens():
    call_command('revoke_expired_tokens')
