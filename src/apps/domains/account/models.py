from django.db import models

from apps.domains.account.constants import GenderType, StatusType
from apps.domains.account.managers import UserManager
from lib.django.db.models.base_model import BaseModel, BaseUserModel, EqualizeMixin


class User(EqualizeMixin, BaseUserModel):
    idx = models.AutoField(primary_key=True, editable=False, verbose_name='u_idx')
    id = models.CharField(max_length=32, unique=True, editable=False, verbose_name='u_id', )

    name = models.CharField(null=True, max_length=32, verbose_name='name')
    reg_date = models.DateTimeField(null=True, verbose_name='reg_date')
    ip = models.CharField(null=True, max_length=16, verbose_name='ip')
    device_id = models.CharField(null=True, max_length=128, verbose_name='device_id')
    email = models.CharField(null=True, max_length=256, verbose_name='email')
    birth_date = models.DateTimeField(null=True, verbose_name='birth_date')
    gender = models.IntegerField(null=True, choices=GenderType.get_choices(), verbose_name='gender')
    verified = models.BooleanField(default=False, verbose_name='verified')
    status = models.IntegerField(null=True, choices=StatusType.get_choices(), verbose_name='status')
    email_verify_date = models.DateTimeField(null=True, verbose_name='email_verify_date')

    USERNAME_FIELD = 'id'

    equal_fields = (
        'idx', 'id', 'name', 'reg_date', 'ip', 'device_id', 'email', 'birth_date', 'gender', 'verified', 'status', 'email_verify_date'
    )

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
