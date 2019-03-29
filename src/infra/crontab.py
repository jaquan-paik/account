from django.core.management import call_command
from uwsgidecorators import lock, timer


@timer(300)
def revoke_expired_tokens(signum: int):
    call_command('revoke_expired_tokens')


@timer(1)
@lock
def set_user_modified_history_order(signum: int):
    call_command('set_user_modified_history_order')


@timer(1)
@lock
def crawl_store_user(signum: int):
    call_command('crawl_store_user')
