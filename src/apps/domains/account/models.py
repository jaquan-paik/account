from django.db import models

from apps.domains.account.managers import UserManager
from lib.django.db.models.base_model import BaseModel, BaseUserModel


class User(BaseUserModel):
    idx = models.AutoField(primary_key=True, editable=False, verbose_name='u_idx')
    id = models.CharField(max_length=32, unique=True, editable=False, verbose_name='u_id', )

    USERNAME_FIELD = 'id'

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = '사용자 계정'
        verbose_name_plural = '사용자 계정 리스트'


class UserModifiedHistory(BaseModel):
    u_idx = models.ForeignKey(User, null=False, on_delete=models.PROTECT, verbose_name='u_idx')
    order = models.BigIntegerField(null=True, db_index=True, verbose_name='히스토리 순서')

    class Meta:
        db_table = 'user_modified_history'
        verbose_name = '사용자 정보 변경 내역'
        verbose_name_plural = '사용자 정보 변경 내역 리스트'


class OAuth2User(BaseModel):
    name = models.CharField(max_length=16, unique=True, verbose_name='이름', )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'oauth2_user'
        verbose_name = 'oauth2 사용자 계정'
        verbose_name_plural = 'oauth2 사용자 계정 리스트'
