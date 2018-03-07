from django.core.management import BaseCommand

from apps.domains.oauth2.services.revoke_token_service import RevokeTokenService


class Command(BaseCommand):
    title = 'Revoke expired tokens'
    help = 'Revoke expired tokens'

    def handle(self, *args, **options) -> None:
        RevokeTokenService.revoke_expired()
