from celery.schedules import crontab

from infra.celery.constants import CeleryQueue


def get_celery_beat_schedule():
    return {
        'revoke-expired-tokens': {
            'task': 'apps.domains.example.tasks.debug_task1',
            'schedule': crontab(hour='4'),
            'args': (),
            'options': {
                'queue': CeleryQueue.LOW
            }
        },
    }
