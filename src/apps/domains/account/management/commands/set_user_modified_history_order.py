from apps.domains.account.services.user_modified_history_service import UserModifiedHistoryService
from lib.django.command import CommonBaseCommand


class Command(CommonBaseCommand):
    title = 'Set user modified history order'
    help = 'Set user modified history order'

    def run(self, *args, **options) -> None:
        UserModifiedHistoryService.set_orders()
