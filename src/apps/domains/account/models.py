from django.db import models

from apps.domains.account.constants import GenderType, StatusType
from apps.domains.account.managers import UserManager
from lib.django.db.models.base_model import BaseModel, BaseUserModel, EqualizeMixin


class User(EqualizeMixin, BaseUserModel):
    idx = models.AutoField(primary_key=True, editable=False, verbose_name='u_idx')
    id = models.CharField(max_length=32, unique=True, editable=False, verbose_name='u_id', )
    name = models.CharField(null=True, max_length=32, verbose_name='name')

    reg_date = models.DateTimeField(null=True, verbose_name='가입일')
    ip = models.GenericIPAddressField(null=True, verbose_name='ip')
    device_id = models.CharField(null=True, max_length=128, verbose_name='device_id')

    email = models.CharField(null=True, max_length=256, verbose_name='email')
    email_verified_date = models.DateTimeField(null=True, verbose_name='이메일 인증 날짜')

    birthday = models.DateTimeField(null=True, verbose_name='생일')
    gender = models.IntegerField(null=True, choices=GenderType.get_choices(), verbose_name='성별')
    is_verified = models.BooleanField(default=False, verbose_name='인증여부')

    status = models.IntegerField(null=True, choices=StatusType.get_choices(), verbose_name='계정 상태')

    USERNAME_FIELD = 'id'

    equal_fields = (
        'idx', 'id', 'name', 'reg_date', 'ip', 'device_id', 'email', 'birthday', 'gender', 'is_verified', 'status', 'email_verified_date'
    )

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = '사용자 계정'
        verbose_name_plural = '사용자 계정 리스트'


class UserModifiedHistory(BaseModel):
    user = models.ForeignKey(User, null=False, db_column='u_idx', to_field='idx', on_delete=models.PROTECT, verbose_name='u_idx')
    order = models.BigIntegerField(null=True, db_index=True, verbose_name='히스토리 순서')

    class Meta:
        db_table = 'user_modified_history'
        verbose_name = '사용자 정보 변경 내역'
        verbose_name_plural = '사용자 정보 변경 내역 리스트'
        index_together = [['id', 'order', ], ]


class OAuth2User(BaseModel):
    name = models.CharField(max_length=16, unique=True, verbose_name='이름', )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'oauth2_user'
        verbose_name = 'oauth2 사용자 계정'
        verbose_name_plural = 'oauth2 사용자 계정 리스트'
