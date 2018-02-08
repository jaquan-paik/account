from datetime import datetime

from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

from apps.domains.account.managers import StaffManager
from lib.django.db.models.base_model import BaseUserModel


class Staff(PermissionsMixin, BaseUserModel):
    email = models.EmailField(max_length=254, unique=True, verbose_name='이메일', )

    is_active = models.BooleanField(default=True, verbose_name='계정 활성화 여부', )
    is_staff = models.BooleanField(default=True, verbose_name='관리자 여부', )
    is_superuser = models.BooleanField(default=True, verbose_name='최고 관리자 여부', )

    last_login = models.DateTimeField(blank=True, null=True, verbose_name='마지막 로그인')
    last_change_password_date = models.DateTimeField(null=True, verbose_name='마지막 패스워드 변경일')

    USERNAME_FIELD = 'email'

    objects = StaffManager()

    def get_full_name(self) -> str:
        return str(self.email)

    def get_short_name(self) -> str:
        return str(self.email)

    def set_password(self, raw_password) -> None:
        super().set_password(raw_password=raw_password)
        self.last_change_password_date = datetime.now()

    class Meta:
        db_table = 'tb_staff'
        verbose_name = '관리자 계정'
        verbose_name_plural = '관리자 계정 리스트'


class User(BaseUserModel):
    email = models.EmailField(max_length=254, unique=True, verbose_name='이메일', )

    is_active = models.BooleanField(default=True, verbose_name='계정 활성화 여부', )

    last_change_password_date = models.DateTimeField(null=True, verbose_name='마지막 패스워드 변경일')

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self) -> str:
        return str(self.email)

    def get_short_name(self) -> str:
        return str(self.email)

    def set_password(self, raw_password) -> None:
        super().set_password(raw_password=raw_password)
        self.last_change_password_date = datetime.now()

    class Meta:
        db_table = 'tb_user'
        verbose_name = '사용자 계정'
        verbose_name_plural = '사용자 계정 리스트'
