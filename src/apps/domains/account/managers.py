from django.contrib.auth.base_user import BaseUserManager

from lib.base.exceptions import ErrorException


class UserManager(BaseUserManager):
    def create_user(self, idx: int, id: str, **kwargs):  # pylint: disable=redefined-builtin
        user = self.model(idx=idx, id=id, **kwargs)
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, idx: int, id: str, **kwargs):  # pylint: disable=redefined-builtin
        raise ErrorException('관리자유저를 회원 테이블에서 만들 수 없습니다.')
