from django.core.management import call_command
from uwsgidecorators import timer


@timer(300)
def revoke_expired_tokens(signum: int):
    call_command('revoke_expired_tokens')
