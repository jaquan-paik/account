from django.db import models

from apps.domains.account.managers import StaffManager, UserManager
from lib.django.db.models.base_model import BaseModel, BaseUserModel


class Staff(BaseUserModel):
    admin_id = models.CharField(max_length=128, unique=True, null=False, verbose_name='어드민 ID')

    USERNAME_FIELD = 'admin_id'

    objects = StaffManager()

    class Meta:
        db_table = 'staff'
        verbose_name = '관리자 계정'
        verbose_name_plural = '관리자 계정 리스트'


class User(BaseUserModel):
    idx = models.AutoField(primary_key=True, editable=False, verbose_name='u_idx')
    id = models.CharField(max_length=16, unique=True, editable=False, verbose_name='u_id', )

    USERNAME_FIELD = 'id'

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = '사용자 계정'
        verbose_name_plural = '사용자 계정 리스트'


class OAuth2User(BaseModel):
    name = models.CharField(max_length=16, unique=True, verbose_name='이름', )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'oauth2_user'
        verbose_name = 'oauth2 사용자 계정'
        verbose_name_plural = 'oauth2 사용자 계정 리스트'
