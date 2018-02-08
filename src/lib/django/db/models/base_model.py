from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        abstract = True


class BaseUserModel(BaseModel, AbstractBaseUser):
    class Meta:
        abstract = True
