from django.core.management import call_command
from uwsgidecorators import timer

from infra.configure.constants import FileLockKeyName
from lib.lock.decorators import f_lock


@timer(300)
def revoke_expired_tokens(signum: int):
    call_command('revoke_expired_tokens')


@timer(1)
@f_lock(FileLockKeyName.SET_USER_MODIFIED_HISTORY_ORDER)
def set_user_modified_history_order(signum: int):
    call_command('set_user_modified_history_order')

# @timer(1)
# @f_lock(FileLockKeyName.CRAWL_STORE_USER)
# def crawl_store_user(signum: int):
#     call_command('crawl_store_user')
