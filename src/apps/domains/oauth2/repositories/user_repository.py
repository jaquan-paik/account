from apps.domains.account.models import User


class UserRepository:
    @staticmethod
    def get_or_create(u_idx: int, u_id: str) -> User:
        user, _ = User.objects.get_or_create(idx=u_idx, id=u_id)
        return user
