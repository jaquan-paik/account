from celery import Celery
from django.conf import settings
from kombu import Queue

from infra.celery.constants import CeleryQueue
from infra.celery.schedules import get_celery_beat_schedule


def generate_celery(site):
    app = Celery('sites.' + site)
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

    # Queue
    # high_Priority: 1초 이내 실행 보장 한다.
    # low_priority: 실행 시점 보장하지 않는다.
    app.conf.task_default_queue = CeleryQueue.LOW
    app.conf.task_queues = (
        Queue(CeleryQueue.LOW),
        Queue(CeleryQueue.HIGH),
    )

    # Extra
    app.conf.update(
        CELERYBEAT_SCHEDULE=get_celery_beat_schedule(),
    )
    return app
