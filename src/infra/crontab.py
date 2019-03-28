from django.core.management import call_command
from uwsgidecorators import timer


@timer(300)
def revoke_expired_tokens(signum: int):
    call_command('revoke_expired_tokens')


@timer(1)
def set_user_modified_history_order(signum: int):
    call_command('set_user_modified_history_order')
