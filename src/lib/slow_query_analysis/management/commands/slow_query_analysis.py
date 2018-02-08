from django.core.management import BaseCommand

from ...service import analyze_slow_query


class Command(BaseCommand):
    title = 'Slow query analysis'
    help = 'Slow query analysis'

    def handle(self, *args, **options) -> None:
        analyze_slow_query()
