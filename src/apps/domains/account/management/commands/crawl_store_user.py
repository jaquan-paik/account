from apps.domains.account.services.crawl_store_user_service import CrawlStoreUserService
from lib.django.command import CommonBaseCommand


class Command(CommonBaseCommand):
    title = 'crawl Store User'
    help = 'crawl Store User'

    def run(self, *args, **options) -> None:
        CrawlStoreUserService.crawl()
