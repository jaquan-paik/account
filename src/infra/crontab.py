from django.core.management import call_command
from uwsgidecorators import timer

from infra.configure.constants import CommandName
from lib.lock.decorators import f_lock


@timer(300)
def revoke_expired_tokens(signum: int):
    call_command(CommandName.REVOKE_EXPIRED_TOKENS)


@timer(1)
@f_lock(CommandName.SET_USER_MODIFIED_HISTORY_ORDER)
def set_user_modified_history_order(signum: int):
    call_command(CommandName.SET_USER_MODIFIED_HISTORY_ORDER)

# @timer(1)
# @f_lock(CommandName.CRAWL_STORE_USER)
# def crawl_store_user(signum: int):
#     call_command(CommandName.CRAWL_STORE_USER)
