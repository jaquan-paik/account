from celery.schedules import crontab

from infra.celery.constants import CeleryQueue


def get_celery_beat_schedule():
    return {
        'revoke-expired-tokens': {
            'task': 'apps.domains.oauth2.tasks.revoke_expired_tokens',
            'schedule': crontab(minute='*'),  # 1분 이내에 테스크 종료될 것이다.
            'args': (),
            'options': {
                'queue': CeleryQueue.LOW
            }
        },
    }
