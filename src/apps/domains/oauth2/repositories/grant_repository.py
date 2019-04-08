from apps.domains.oauth2.models import Grant, Application as Client


class GrantRepository:

    @classmethod
    def create_grant(cls, client: Client, redirect_uri: str, u_idx: int, scope: str) -> Grant:
        grant = Grant(user_id=u_idx, application=client, redirect_uri=redirect_uri, scope=scope)
        grant.save()
        return grant

    @staticmethod
    def get_grant_by_code(code: str) -> Grant:
        grant = Grant.objects.get(code=code)
        return grant
