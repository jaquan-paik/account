from django.db import models

from lib.django.db.models.base_model import BaseModel
from .managers import EmailBlacklistManager


class AbstractEmailBlacklist(BaseModel):
    email = models.EmailField(max_length=254, db_index=True, verbose_name='이메일', )
    is_active = models.BooleanField(null=False, default=True, db_index=True, verbose_name='활성화 여부', )

    objects = EmailBlacklistManager()

    class Meta:
        abstract = True
        db_table = 'email_blacklist'
        verbose_name = '이메일 블랙리스트'
        verbose_name_plural = '이메일 블랙리스트'


class EmailBlacklist(AbstractEmailBlacklist):
    class Meta(AbstractEmailBlacklist.Meta):
        swappable = 'EMAIL_BLACKLIST_MODEL'
