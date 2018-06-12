from apps.domains.oauth2.services.revoke_token_service import RevokeTokenService
from lib.django.command import CommonBaseCommand


class Command(CommonBaseCommand):
    title = 'Revoke expired tokens'
    help = 'Revoke expired tokens'

    def run(self, *args, **options) -> None:
        RevokeTokenService.revoke_expired()
